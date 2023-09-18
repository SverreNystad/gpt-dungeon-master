import logging
from src.text_generation.chat_gpt import chat_with_gpt
from src.npc_generation import Alignment, Race, generate_alignment, generate_general_background, generate_npc, generate_npc_relations
from src.text_to_image.image_generator import generate_image_request, ImageSize

# Set up logging
logging.basicConfig(filename='gpt_dungeon_master.log',
                    level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Create a logger instance for this script
logger = logging.getLogger(__name__)

# Run chat_gpt.py
logger.info("Running non_player_character_generation.py generating npc")
npc = generate_npc()
logger.info(npc)

# Run image_generation.py
logger.info("Running image_generation.py")
image_result = generate_image_request(prompt=npc.appearance, number_of_images=1, size=ImageSize(1024,1024))
logger.info(image_result)
