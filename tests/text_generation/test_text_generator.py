import pytest
from src.text_generation.text_generator import get_default_text_generator, TextGenerator, LLM, Chatbot

@pytest.mark.apitest
def test_text_generator():
    prompt = "Say anything!"
    generator: TextGenerator = get_default_text_generator()
    result = generator.predict(prompt)
    assert result is not None, "The result was None"