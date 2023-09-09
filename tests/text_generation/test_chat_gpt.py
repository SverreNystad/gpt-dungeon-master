import pytest
import src.text_generation.chat_gpt as chat_gpt

def test_chat_gpt_response():
    prompt = "Say anything!"
    response = chat_gpt.chat_gpt(prompt)
    assert response