from dataclasses import dataclass
import requests
from src.text_to_image.config import ImageConfig

@dataclass(init=False)
class ImageSize:
    """
    Represents the size of an image.
    The size of the generated images. Must be one of 256x256, 512x512, or 1024x1024.
    """
    width: int
    height: int

    def __init__(self, width: int=256, height: int=256) -> None:
        if (width < 0) or (height < 0):
            raise ValueError("Width and height must be positive.")
        if (width not in [256, 512, 1024]) or (height not in [256, 512, 1024]):
            raise ValueError("Width and height must be one of 256, 512, or 1024.")
        if width != height:
            raise ValueError("Width and height must be the same.")
        self.width = width
        self.height = height

    def __repr__(self) -> str:
        return f"{self.width}x{self.height}"
    
    def __str__(self) -> str:
        return f"{self.width}x{self.height}"

def generate_image_request(prompt: str, number_of_images: int=1, size: ImageSize=ImageSize(256,256)) -> str:
    """
    Generates an image based on the given prompt.
    Args:
        :param prompt (str): A text description of the desired image(s). The maximum length is 1000 characters.
        :param number_of_images (int): The number of images to generate. Defaults to 1, cant be more than 10 or less than 1.
        :param size (ImageSize): The size of the generated images. Must be one of 256x256, 512x512, or 1024x1024.
    Returns:
        :return: A JSON object containing the generated image(s).
    """
    if not (1 <= number_of_images <= 10):
        raise ValueError("Number of images must be between 1 and 10.")
    
    if len(prompt) > 1000 or len(prompt) < 1:
        raise ValueError("Prompt must be at least 1 character or less than 1000 characters.")
    
    if not isinstance(size, ImageSize):
        raise TypeError("Size must be an instance of ImageSize.")

    URL = ImageConfig().URL
    API_KEY = ImageConfig().API_KEY
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {API_KEY}',
    }

    data = {
        'prompt': prompt,
        'n': number_of_images,
        'size': str(size),
    }

    response = requests.post(URL, headers=headers, json=data)
    return response.json()

