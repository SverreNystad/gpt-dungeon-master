import pytest
from src.text_generation.text_generator import get_default_text_generator, TextGenerator, LLM, Chatbot

@pytest.mark.apitest
def test_get_default_text_generator():
    generator: TextGenerator = get_default_text_generator()
    assert generator is not None, "The generator was None"
    assert isinstance(generator, TextGenerator), "The generator was not an TextGenerator"

def test_LLM():
    generator: TextGenerator = LLM("DUMMY_KEY")
    assert isinstance(generator, TextGenerator), "The generator was not an TextGenerator"

def test_Chatbot():
    generator: TextGenerator = Chatbot("DUMMY_KEY")
    assert isinstance(generator, TextGenerator), "The generator was not an TextGenerator"


@pytest.mark.apitest
def test_text_generator():
    prompt = "Say anything!"
    generator: TextGenerator = get_default_text_generator()
    result = generator.predict(prompt)
    assert result is not None, "The result was None"