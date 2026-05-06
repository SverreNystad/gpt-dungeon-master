import torch
from PIL.Image import Image
from diffusers import FluxPipeline

def generate_image_with_hf_api() -> Image:
    import os
    from huggingface_hub import InferenceClient

    client = InferenceClient(
        provider="auto",
        api_key=os.environ["HF_TOKEN"],
    )

    # output is a PIL.Image object
    image = client.text_to_image(
        "Astronaut riding a horse",
        model="black-forest-labs/FLUX.1-dev:fastest",
    )
    return image

if __name__ == "__main__":
    pipe = FluxPipeline.from_pretrained("black-forest-labs/FLUX.1-dev", torch_dtype=torch.bfloat16)
    # pipe.enable_model_cpu_offload() #save some VRAM by offloading the model to CPU. Remove this if you have enough GPU power

    prompt = "A goblin in its dark cave, digital art, fantasy, highly detailed, cinematic lighting"
    image = pipe(
        prompt,
        height=1024,
        width=1024,
        guidance_scale=3.5,
        num_inference_steps=50,
        max_sequence_length=512,
        generator=torch.Generator("cpu").manual_seed(0)
    ).images[0]
    image.save("flux-dev.png")


