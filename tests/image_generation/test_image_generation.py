import pytest
import sys
sys.path.append('C:/Users/Bruker/OneDrive/koding/gpt-dungeon-master')  # path to the root of your project

from src.image_generation.image_generation import generate_image_request, ImageSize

def test_image_generation_not_supported_size():
    with pytest.raises(ValueError):
        wrong_size = ImageSize(100, 100)
        correct_prompt = "A painting of a dungeon master sitting at a table with a group of adventurers playing Dungeons and Dragons."
        generate_image_request(prompt=correct_prompt, size=wrong_size)

def test_image_generation_with_wrong_size():
    with pytest.raises(ValueError):
        wrong_size = ImageSize(256, 512)
        correct_prompt = "A painting of a dungeon master sitting at a table with a group of adventurers playing Dungeons and Dragons."
        generate_image_request(prompt=correct_prompt, size=wrong_size)

def test_image_generation_with_negative_size():
    with pytest.raises(ValueError):
        negative_legal_size = ImageSize(-256, -256)
        correct_prompt = "A painting of a dungeon master sitting at a table with a group of adventurers playing Dungeons and Dragons."
        generate_image_request(prompt=correct_prompt, size=negative_legal_size)

def test_image_generation_with_negative_amount_of_pictures():
    to_few_images = -1
    with pytest.raises(ValueError):
        generate_image_request(prompt="test", number_of_images=to_few_images)

def test_image_generation_with_no_amount_of_pictures():
    no_images = 0
    with pytest.raises(ValueError):
        generate_image_request(prompt="test", number_of_images=no_images)


def test_image_generation_with_too_many_pictures():
    to_many_images = 11
    with pytest.raises(ValueError):
        generate_image_request(prompt="test", number_of_images=to_many_images)
    

def test_image_generation_with_too_long_prompt():
    prompt = 10000 * "a"
    with pytest.raises(ValueError):
        generate_image_request(prompt=prompt)

def test_image_generation_with_too_short_prompt():
    prompt = ""
    with pytest.raises(ValueError):
        generate_image_request(prompt=prompt)


def test_image_generation_with_wrong_type_of_size():
    wrong_type_size = "256x256"
    with pytest.raises(TypeError):
        generate_image_request(prompt="test", size=wrong_type_size)


def test_correct_image_generation():
    correct_prompt = "A painting of a dungeon master sitting at a table with a group of adventurers playing Dungeons and Dragons."
    
    response = generate_image_request(prompt=correct_prompt)

    assert response["data"] != None

def test_correct_image_generation_with_size():
    correct_prompt = "A painting of a dungeon master sitting at a table with a group of adventurers playing Dungeons and Dragons."
    correct_size = ImageSize(512, 512)

    response = generate_image_request(prompt=correct_prompt, size=correct_size)

    assert response["data"] != None

def test_correct_image_generation_when_generating_several_pictures():
    correct_prompt = "A painting of a dungeon master sitting at a table with a group of adventurers playing Dungeons and Dragons."
    correct_amount_of_images = 2

    response = generate_image_request(prompt=correct_prompt, number_of_images=correct_amount_of_images)

    assert response["data"] != None
    assert len(response["data"]) == correct_amount_of_images