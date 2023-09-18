import pytest
import src.text_generation.text_generator as text_generator

@pytest.mark.apitest
def test_chat_gpt_response():
    prompt = "Say anything!"
    response = text_generator.chat_with_gpt(prompt)
    assert response