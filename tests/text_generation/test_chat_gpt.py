import pytest
import src.text_generation.chat_gpt as chat_gpt

@pytest.mark.apitest
def test_chat_gpt_response():
    prompt = "Say anything!"
    response = chat_gpt.chat_with_gpt(prompt)
    assert response