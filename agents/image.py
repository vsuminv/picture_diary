import os
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()


def generate_image(prompt: str, output_path: str, model: str = "dalle") -> str:
    Path("outputs").mkdir(exist_ok=True)

    if model == "flux":
        import fal_client

        result = fal_client.subscribe(
            "fal-ai/flux/schnell",
            arguments={"prompt": prompt, "num_images": 1, "image_size": "landscape_4_3"},
        )
        image_url = result["images"][0]["url"]
        response = requests.get(image_url, timeout=30)
        with open(output_path, "wb") as f:
            f.write(response.content)
    else:
        from openai import OpenAI

        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        image_url = response.data[0].url
        img_data = requests.get(image_url, timeout=30).content
        with open(output_path, "wb") as f:
            f.write(img_data)

    return output_path
