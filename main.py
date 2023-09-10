from src.image_generation.image_generation import generate_image_request, ImageSize

# Run image_generation.py
print("Running image_generation.py")
result = generate_image_request(prompt="A painting of a dungeon master sitting at a table with a group of adventurers playing Dungeons and Dragons.")
print(result)

