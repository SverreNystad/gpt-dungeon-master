#!/usr/bin/env python3
import asyncio
from openai import AsyncOpenAI
import os

api_key = os.environ.get("OPENAI_API_KEY")

aclient = AsyncOpenAI(api_key=api_key)


# ---------------------------------------------------------
# 1. HELPER FUNCTION: CHUNK THE TEXT
# ---------------------------------------------------------
def chunk_text(text, max_chars: int):
    """
    Split the text into chunks of up to `max_chars` characters.
    Adjust `max_chars` to fit within your model's context window.
    """
    chunks = []
    start = 0
    while start < len(text):
        end = start + max_chars
        chunks.append(text[start:end])
        start = end
    return chunks


# ---------------------------------------------------------
# 2. ASYNC FUNCTION: CONVERT A SINGLE CHUNK TO MARKDOWN
# ---------------------------------------------------------
async def convert_chunk_to_markdown(chunk, model="gpt-4o-mini"):
    """
    Sends one chunk of text to the OpenAI Chat API (async) to be converted to Markdown.
    """
    response = await aclient.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful assistant that converts plain text documents "
                    "to Markdown, ensuring proper headers, tables, lists, etc."
                ),
            },
            {
                "role": "user",
                "content": (
                    "Convert the following text to Markdown, ensuring correct syntax:\n\n"
                    f"{chunk}"
                ),
            },
        ],
        temperature=0.0,
    )
    markdown_text = response.choices[0].message.content.strip()
    return markdown_text


# ---------------------------------------------------------
# 3. ASYNC FUNCTION: CONVERT LARGE DOCUMENT TO MARKDOWN
# ---------------------------------------------------------
async def convert_large_document_to_markdown_async(
    input_file_path: str,
    output_file_path: str,
    model: str,
):
    """
    Reads a (potentially very large) text file, splits it into chunks,
    uses async calls to convert each chunk to Markdown, and writes the
    combined Markdown to an output file.

    :param input_file_path: Path to the input text file.
    :param output_file_path: Path to the output Markdown file.
    :param openai_api_key: Your OpenAI API key.
    :param model: OpenAI model to use. Defaults to gpt-3.5-turbo.
    """

    # 1. Read the entire input file
    with open(input_file_path, "r", encoding="utf-8") as f:
        full_text = f.read()

    # 2. Split the text into manageable chunks
    text_chunks = chunk_text(full_text, max_chars=5000)

    # 3. Create asyncio tasks for each chunk
    tasks = []
    for i, chunk in enumerate(text_chunks, start=1):
        print(f"Scheduling conversion for chunk {i} of {len(text_chunks)}...")
        tasks.append(asyncio.create_task(convert_chunk_to_markdown(chunk, model=model)))

    # 4. Gather all results concurrently
    all_markdown_chunks = await asyncio.gather(*tasks)

    # 5. Combine all converted chunks into one final Markdown
    final_markdown = "\n\n".join(all_markdown_chunks)

    # 6. Write the combined Markdown to the output file
    with open(output_file_path, "w", encoding="utf-8") as f:
        f.write(final_markdown)

    print(f"\nConversion complete! Markdown written to: {output_file_path}")


# ---------------------------------------------------------
# 4. MAIN ENTRY POINT
# ---------------------------------------------------------
if __name__ == "__main__":

    input_file = "new_rules.txt"
    output_file = "output_2.md"
    chosen_model = "gpt-4o"

    # Use asyncio.run() to execute our asynchronous function
    asyncio.run(
        convert_large_document_to_markdown_async(
            input_file_path=input_file,
            output_file_path=output_file,
            model=chosen_model,
        )
    )
