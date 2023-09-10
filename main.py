from src.text_generation.chat_gpt import chat_with_gpt
from src.image_generation.image_generation import generate_image_request, ImageSize

# Run chat_gpt.py
print("Running chat_gpt.py")
prompt = input("Enter your prompt: ")
gpt_response = chat_with_gpt(prompt)
print(gpt_response)

# Run image_generation.py
print("Running image_generation.py")
image_result = generate_image_request(prompt="A painting of a dungeon master sitting at a table with a group of adventurers playing Dungeons and Dragons.")
print(image_result)

