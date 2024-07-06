import logging
from src.npc_generation import Alignment, Race, generate_alignment, generate_general_background, generate_npc, generate_npc_relations
from src.text_to_image.image_generator import generate_image_request, ImageSize
from src.agents.dungeon_master import run_dungeon_master

# Set up logging
logging.basicConfig(filename='gpt_dungeon_master.log',
                    level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Create a logger instance for this script
logger = logging.getLogger(__name__)


# Run dungeon master agent
logger.info("Running dungeon_master.py")
while True:
    prompt = input("The GPT Dungeon Master awaits your input: ")

    answer = run_dungeon_master(prompt=prompt)
    print(answer)
    logger.info(f"Prompt: {prompt}, Answer: {answer}")

logger.info("Finished running dungeon_master.py")