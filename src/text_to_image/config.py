import os
from dotenv import load_dotenv

load_dotenv()

class ImageConfig:
    API_KEY = os.getenv('OPENAI_DALL_E_API_KEY')
    MODEL_NAME = "dall-e-turbo-0613"

    URL = "https://api.openai.com/v1/images/generations"