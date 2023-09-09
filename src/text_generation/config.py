import os
from dotenv import load_dotenv

load_dotenv()

class GPTConfig:

    API_KEY = os.getenv('OPENAI_API_KEY')

if __name__ == "__main__":
    print(GPTConfig.API_KEY)