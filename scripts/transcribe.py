#!/usr/bin/env python3
from openai import OpenAI
import asyncio

import os

API_KEY = os.environ.get("OPENAI_API_KEY")
client = OpenAI(
    api_key=API_KEY,
)


def chunk_text(text, max_chars=12000):
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


def convert_chunk_to_markdown(chunk, model="gpt-3.5-turbo"):
    """
    Sends one chunk of text to the OpenAI Chat API to be converted to Markdown.
    """
    response = client.chat.completions.create(
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


def convert_large_document_to_markdown(
    input_file_path: str,
    output_file_path: str,
    openai_api_key: str,
    model: str = "gpt-4o-mini",
):
    """
    Reads a (potentially very large) text file, splits it into chunks,
    converts each chunk to Markdown using OpenAI, and writes the combined
    Markdown to an output file.

    :param input_file_path: Path to the input text file.
    :param output_file_path: Path to the output Markdown file.
    :param openai_api_key: Your OpenAI API key.
    :param model: OpenAI model to use. Defaults to gpt-3.5-turbo.
    """
    # Set your OpenAI API key

    # 1. Read the entire input file
    with open(input_file_path, "r", encoding="utf-8") as f:
        full_text = f.read()

    # 2. Split the text into manageable chunks
    #    Adjust max_chars depending on your model and typical input size.
    text_chunks = chunk_text(full_text, max_chars=12000)

    # 3. Convert each chunk to Markdown, then combine
    all_markdown_chunks = []
    for i, chunk in enumerate(text_chunks, start=1):
        print(f"Converting chunk {i} of {len(text_chunks)}...")
        markdown_chunk = convert_chunk_to_markdown(chunk, model=model)
        all_markdown_chunks.append(markdown_chunk)

    # 4. Combine all converted chunks into one final Markdown
    final_markdown = "\n\n".join(all_markdown_chunks)

    # 5. Write the combined Markdown to the output file
    with open(output_file_path, "w", encoding="utf-8") as f:
        f.write(final_markdown)

    print(f"\nConversion complete! Markdown written to: {output_file_path}")


if __name__ == "__main__":
    # 2. Update 'input.txt' and 'output.md' paths as needed
    convert_large_document_to_markdown(
        input_file_path="new_rules.txt",
        output_file_path="output.md",
        openai_api_key="YOUR_OPENAI_API_KEY",
    )
