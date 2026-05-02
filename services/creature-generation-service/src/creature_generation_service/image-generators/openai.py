


if __name__ == "__main__":
    from openai import OpenAI
    import base64

    client = OpenAI() 

    response = client.responses.create(
        model="gpt-5.5",
        input="Generate an image of gray tabby cat hugging an otter with an orange scarf",
        tools=[{"type": "image_generation"}],
    )

    # Save the image to a file
    image_data = [
        output.result
        for output in response.output
        if output.type == "image_generation_call"
    ]
        
    if image_data:
        image_base64 = image_data[0]
        with open("otter.png", "wb") as f:
            f.write(base64.b64decode(image_base64))