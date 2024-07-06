import os
from dotenv import load_dotenv

load_dotenv()

class GPTConfig:

    API_KEY = os.getenv('OPENAI_API_KEY')
    MODEL_NAME = "gpt-3.5-turbo-0613"
