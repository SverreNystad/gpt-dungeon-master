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

    def __init__(self, api_key: str=None):
        self.__api_key = GPTConfig.API_KEY if api_key is None else api_key
        self.__llm = OpenAI(openai_api_key=self.__api_key)

    def predict(self, prompt: str) -> str:
        """Predict the next word based on the prompt."""
        return self.__llm.predict(prompt)

class Chatbot(TextGenerator):
    """A chatbot that can chat with a user."""

    def __init__(self, api_key: str=None):
        self.__api_key = GPTConfig.API_KEY if api_key is None else api_key
        self.__chatbot = ChatOpenAI(openai_api_key=self.__api_key)


    def predict(self, prompt: str) -> str:
        """Chat with the chatbot."""
        return self.__chatbot.predict(prompt)

def get_default_text_generator() -> TextGenerator:
    """Return the default text generator."""
    api_key = GPTConfig.API_KEY
    return LLM(api_key=api_key)
