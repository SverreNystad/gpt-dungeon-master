#!/usr/bin/env python3
"""
sparc3d_automation.py - Browser automation for Hitem3D's Sparc3D web demo.

The Hugging Face Space (ilcve21/Sparc3D) is just an iframe wrapper around
https://3dserver.hitem3d.ai/, so this script automates that site directly.

Setup (one-time)
----------------
    pip install playwright
    playwright install chromium

    # First run: opens a real browser. Log in / dismiss popups / accept ToS,
    # then come back to the terminal and press Enter. Session is persisted to
    # ~/.sparc3d_automation so you don't have to log in again.
    python sparc3d_automation.py --setup

Normal use
----------
    python sparc3d_automation.py path/to/photo.jpg -o cat.glb

Tweak selectors
---------------
If the script can't find the Generate or Download button, run with --inspect.
This launches Playwright Inspector — point at any element and copy its
selector into the constants at the top of this file.

    python sparc3d_automation.py path/to/photo.jpg --inspect

Other useful flags
------------------
    --headed         Show the browser window (default: headless)
    --timeout MIN    Override generation timeout in minutes (default: 10)
"""

from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

from playwright.async_api import (
    async_playwright,
    BrowserContext,
    Page,
    TimeoutError as PWTimeout,
)


URL = "https://3dserver.hitem3d.ai/"
USER_DATA_DIR = Path.home() / ".sparc3d_automation"

# --------------------------------------------------------------------------
# Selectors — adjust these once you've confirmed them with --inspect.
# Prefer role+name (robust against CSS class churn) over raw CSS selectors.
# --------------------------------------------------------------------------
FILE_INPUT_SELECTOR = 'input[type="file"]'

# This site uses Vue-styled <div>s rather than real <button>s, so role-based
# queries miss them. Each entry below is tried as a Playwright selector in
# order — the first one to find a visible element wins.
#
# Cheat sheet:
#   ".btn-generate"            -> CSS class
#   "text=Generate"            -> exact visible text
#   "div.btn-generate >> text=Generate"  -> compound
#   '[data-testid="gen"]'      -> data attribute
GENERATE_SELECTORS = [
    ".btn-generate",
    "text=Generate",
    "text=Create",
    "text=Run",
    "text=Start",
    "text=Submit",
]
DOWNLOAD_SELECTORS = [
    ".btn-download",
    ".btn-export",
    "text=Download GLB",
    "text=Download",
    "text=Export",
    "text=Save",
    "text=GLB",
]
# If clicking Download opens a format picker:
GLB_OPTION_TEXTS = ["GLB", ".glb", "glb"]


# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------


async def _click_first_match(
    page: Page, selectors: list[str], timeout: int = 5_000
) -> str:
    """Try each selector in order; click the first that resolves to a visible element."""
    for sel in selectors:
        loc = page.locator(sel).first
        try:
            if await loc.count() > 0 and await loc.is_visible():
                await loc.click(timeout=timeout)
                return sel
        except PWTimeout:
            continue
        except Exception:
            continue
    raise RuntimeError(f"No selector matched a visible element: {selectors}")


async def _wait_for_any(page: Page, selectors: list[str], timeout_ms: int):
    """Poll until any selector resolves to a visible element. Return (locator, selector)."""
    deadline = asyncio.get_event_loop().time() + timeout_ms / 1000
    while asyncio.get_event_loop().time() < deadline:
        for sel in selectors:
            loc = page.locator(sel).first
            try:
                if await loc.count() > 0 and await loc.is_visible():
                    return loc, sel
            except Exception:
                pass
        await asyncio.sleep(1.0)
    raise RuntimeError(
        f"None of these selectors became visible within {timeout_ms / 1000:.0f}s: {selectors}"
    )


# --------------------------------------------------------------------------
# Modes
# --------------------------------------------------------------------------


async def setup_session() -> None:
    USER_DATA_DIR.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as p:
        ctx = await p.chromium.launch_persistent_context(
            USER_DATA_DIR.as_posix(),
            headless=False,
            accept_downloads=True,
        )
        page = ctx.pages[0] if ctx.pages else await ctx.new_page()
        await page.goto(URL)
        print("\n" + "=" * 64)
        print(" Browser is open. Log in, accept any cookie/ToS prompts, etc.")
        print(" When you're ready (still on the working app page), press Enter.")
        print("=" * 64 + "\n")
        # Block on stdin without freezing the event loop:
        await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)
        await ctx.close()
        print(f"Session saved to {USER_DATA_DIR}")


async def run(
    image_path: Path, output_path: Path, headless: bool, inspect: bool, timeout_min: int
) -> None:
    USER_DATA_DIR.mkdir(parents=True, exist_ok=True)
    timeout_ms = timeout_min * 60 * 1000

    async with async_playwright() as p:
        ctx: BrowserContext = await p.chromium.launch_persistent_context(
            USER_DATA_DIR.as_posix(),
            headless=headless and not inspect,
            accept_downloads=True,
        )
        page = ctx.pages[0] if ctx.pages else await ctx.new_page()
        page.set_default_timeout(60_000)

        await page.goto(URL, wait_until="domcontentloaded")

        if inspect:
            print(
                "[inspect] Playwright Inspector is open. Explore selectors, then "
                "click 'Resume' to let the script continue."
            )
            await page.pause()

        # 1) Upload — this works even when the file input is visually hidden
        #    behind a styled drop zone, which is the common pattern.
        print(f"[1/4] Uploading {image_path.name} ...")
        file_input = page.locator(FILE_INPUT_SELECTOR).first
        await file_input.wait_for(state="attached", timeout=30_000)
        await file_input.set_input_files(str(image_path))

        # 2) Trigger generation
        print("[2/4] Clicking Generate ...")
        clicked_sel = await _click_first_match(page, GENERATE_SELECTORS, timeout=10_000)
        print(f"      (matched {clicked_sel!r})")

        # 3) Wait for processing to finish.
        print(f"[3/4] Generating (timeout {timeout_min} min) ...")
        download_btn, found_sel = await _wait_for_any(
            page, DOWNLOAD_SELECTORS, timeout_ms
        )
        print(f"      Generation finished; matched {found_sel!r}")

        # 4) Trigger and capture the download. expect_download() catches
        #    direct downloads, blob URLs, and fetch-then-save patterns.
        print("[4/4] Downloading GLB ...")
        async with page.expect_download(timeout=120_000) as dl_info:
            await download_btn.click()
            # If clicking opens a format menu instead of starting a download,
            # try to click a GLB option. Failures here are non-fatal — the
            # original click may already have triggered a download.
            for txt in GLB_OPTION_TEXTS:
                try:
                    opt = page.get_by_text(txt, exact=True).first
                    if await opt.is_visible(timeout=1500):
                        await opt.click(timeout=2000)
                        break
                except Exception:
                    continue
        download = await dl_info.value

        output_path.parent.mkdir(parents=True, exist_ok=True)
        await download.save_as(str(output_path))
        print(f"      Saved -> {output_path.resolve()}")

        await ctx.close()


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------


def main() -> None:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("image", nargs="?", help="Path to input image (PNG/JPG)")
    ap.add_argument(
        "-o",
        "--output",
        default="output.glb",
        help="Output GLB path (default: output.glb)",
    )
    ap.add_argument(
        "--setup", action="store_true", help="One-time login / session setup"
    )
    ap.add_argument(
        "--inspect",
        action="store_true",
        help="Open Playwright Inspector to find selectors",
    )
    ap.add_argument("--headed", action="store_true", help="Show browser window")
    ap.add_argument(
        "--timeout",
        type=int,
        default=100,
        help="Generation timeout in minutes (default: 10)",
    )
    args = ap.parse_args()

    if args.setup:
        asyncio.run(setup_session())
        return

    if not args.image:
        ap.error("image is required (or use --setup first)")
    image_path = Path(args.image).expanduser()
    if not image_path.exists():
        ap.error(f"image not found: {image_path}")

    asyncio.run(
        run(
            image_path=image_path,
            output_path=Path(args.output).expanduser(),
            headless=not args.headed,
            inspect=args.inspect,
            timeout_min=args.timeout,
        )
    )


if __name__ == "__main__":
    main()
