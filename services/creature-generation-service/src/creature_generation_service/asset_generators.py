from typing import Protocol
from PIL import Image

class ImageGenerator(Protocol):
    def generate_image(self, description: str) -> Image:
        """Generates an image based on the provided description."""
        ...

class ModelGenerator(Protocol):
    def generate_3d_model(self, image: Image) -> bytes:
        """Generates a 3D model based on the provided image."""
        ...