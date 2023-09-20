from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from src.text_generation.config import GPTConfig
from abc import ABC, ABCMeta, abstractmethod

class TextGenerator(ABC):
    """A text generator that can generate text based on a prompt."""
    
    @classmethod
    def __instancecheck__(cls, instance):
        return cls.__subclasscheck__(type(instance))
    
    @classmethod
    def __subclasscheck__(cls: ABCMeta, subclass: type) -> bool:
        return (hasattr(subclass, 'predict') and 
                callable(subclass.predict))

    @abstractmethod
    def predict(self, prompt: str) -> str:
        """Predict the next word based on the prompt."""
        pass

class LLM(TextGenerator):
    """A text generator that uses the Language Model API from OpenAI."""

    def __init__(self, api_key: str=None, temperature: float=0.0):
        self.__api_key = GPTConfig.API_KEY if api_key is None else api_key
        self.__llm = OpenAI(openai_api_key=self.__api_key, temperature=temperature)

    def predict(self, prompt: str) -> str:
        """Predict the next word based on the prompt."""
        return self.__llm.predict(prompt)

class Chatbot(TextGenerator):
    """A chatbot that can chat with a user."""

    def __init__(self, api_key: str=None, temperature: float=0.7):
        self.__api_key = GPTConfig.API_KEY if api_key is None else api_key
        self.__chatbot = ChatOpenAI(openai_api_key=self.__api_key, temperature=temperature)


    def predict(self, prompt: str) -> str:
        """Chat with the chatbot."""
        return self.__chatbot.predict(prompt)

def get_default_text_generator(temperature: float = 0.7, is_llm: bool = True) -> TextGenerator:
    """Return the default text generator.
    Args:
        temperatur (float): The temperature of the text generation. Must be between 0.0 and 1.0. 
        It is focused on the most likely tokens when set to 0.0 and focused on the most creative tokens when set to 1.0.
        is_llm (bool): Whether to use the LLM or the Chatbot. True for LLM, False for Chatbot.
    Returns:
        :return: A text generator.
    """
    assert 0.0 <= temperature <= 1.0, "Temperature must be between 0.0 and 1.0"
    if is_llm:
        return LLM(temperature)
    else:
        return Chatbot(temperature)

