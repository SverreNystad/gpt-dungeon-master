from dataclasses import dataclass
import requests
from config import ImageConfig

@dataclass(init=False)
class ImageSize:
    """
    Represents the size of an image.
    The size of the generated images. Must be one of 256x256, 512x512, or 1024x1024.
    """
    width: int
    height: int

    def __init__(self, width: int=256, height: int=256) -> None:
        assert width == height, "Width and height must be the same."
        assert width in [256, 512, 1024], "Width and height must be one of 256, 512, or 1024."
        self.width = width
        self.height = height

    def __repr__(self) -> str:
        return f"{self.width}x{self.height}"
    def __str__(self) -> str:
        return f"{self.width}x{self.height}"

def generate_image(prompt: str, number_of_images: int=1, size: ImageSize=ImageSize(256,256)) -> str:
    """
    Generates an image based on the given prompt.
    Args:
    :param prompt: A text description of the desired image(s). The maximum length is 1000 characters.
    :param number_of_images: The number of images to generate. Defaults to 1, cant be more than 10 or less than 1.
    :param size: The size of the generated images. Must be one of 256x256, 512x512, or 1024x1024.
    """
    assert number_of_images <= 10 and number_of_images >= 1, "Number of images must be between 1 and 10."
    assert len(prompt) <= 1000, "Prompt must be less than 1000 characters."
    assert isinstance(size, ImageSize), "Size must be an instance of ImageSize."

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

print(generate_image(prompt="A painting of a dungeon master sitting at a table with a group of adventurers playing Dungeons and Dragons."))