from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
import json
import base64

load_dotenv()

client = OpenAI()

Path("outputs").mkdir(exist_ok=True)
Path("domains").mkdir(exist_ok=True)

travel_place = {
    "location": "Eiffel Tower, Paris",
    "description": (
        "파리 에펠탑을 배경으로 한 도시 여행 장면, "
        "감성적인 여행자의 시선으로 바라본 풍경"
    )
}


TIME_VARIANTS = {
    "golden_hour": {
        "lighting": "warm golden sunset light",
        "sky": "orange and pink sunset sky",
        "mood": "warm emotional evening atmosphere"
    },
    "blue_hour": {
        "lighting": "cool blue ambient twilight light",
        "sky": "deep blue twilight sky",
        "mood": "calm cinematic night atmosphere"
    }
}

PROMPT_STYLE = {
    "shot": "wide shot",
    "angle": "eye-level",
    "lens_or_style": "35mm travel photography",
    "mood": "cinematic instagram travel style"
}


def build_travel_prompt(location: str, description: str, time_key: str) -> str:

    variant = TIME_VARIANTS[time_key]

    return f"""
{location}
{description}

{variant['sky']}
{variant['lighting']}
{variant['mood']}

cinematic travel photography,
35mm lens,
ultra realistic,
high detail,
instagram travel aesthetic
"""


def save_b64_image(b64_data: str, save_path: Path) -> str:

    save_path.parent.mkdir(parents=True, exist_ok=True)

    save_path.write_bytes(
        base64.b64decode(b64_data)
    )

    return str(save_path)


def generate_travel_image(prompt: str, output_path: str) -> str:

    result = client.images.generate(
        model="gpt-image-1.5",
        prompt=prompt,
        size="1024x1024",
        quality="auto",
        n=1
    )

    b64_data = result.data[0].b64_json

    return save_b64_image(
        b64_data,
        Path(output_path)
    )



def save_travel_json():

    scenes = []

    for idx, time_key in enumerate(TIME_VARIANTS.keys(), start=1):

        scenes.append({
            "id": f"scene_{idx:02d}",
            "diary_sentence": f"{travel_place['location']}의 {time_key} 분위기",
            "visual_focus": travel_place["location"],
            "prompt_addons": [
                time_key,
                "travel photography",
                "cinematic lighting"
            ],
            "negative_prompt": "blur, text, watermark"
        })

    data = {
        "domain": "travel",
        "version": "day5",
        "prompt_style": PROMPT_STYLE,
        "scenes": scenes
    }

    Path("domains").mkdir(exist_ok=True)

    with open("domains/travel_prompts.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("JSON 저장 완료 -> domains/travel_prompts.json")



if __name__ == "__main__":

    save_travel_json()

    for idx, time_key in enumerate(TIME_VARIANTS.keys(), start=1):

        prompt = build_travel_prompt(
            location=travel_place["location"],
            description=travel_place["description"],
            time_key=time_key
        )

        output_path = f"outputs/travel_{idx}.png"

        print(f"\n생성 중: {time_key}")

        image_path = generate_travel_image(
            prompt=prompt,
            output_path=output_path
        )

        print(f"저장 완료: {image_path}")