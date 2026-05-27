from pathlib import Path

from dotenv import load_dotenv

from agents.image import generate_image

load_dotenv()

Path("outputs").mkdir(exist_ok=True)

TIME_VARIANTS: dict[str, dict] = {
    "golden_hour": {
        "lighting": "warm golden sunset light, amber glow, long soft shadows",
        "mood": "warm, romantic, nostalgic, glowing",
        "color_palette": "golden yellows, warm oranges, soft reds, honey tones",
    },
    "blue_hour": {
        "lighting": "cool twilight blue light, city lights just turning on, dusk",
        "mood": "serene, mysterious, ethereal, contemplative",
        "color_palette": "deep indigo blues, cool purples, silver whites, electric blue",
    },
}

BASE_SCENE: str = (
    "A scenic travel landscape of a coastal village with traditional architecture, "
    "boats in harbor, cobblestone streets, "
    "professional travel photography, ultra detailed, cinematic composition, 8K"
)


def build_travel_prompt(base_scene: str, time_of_day: str) -> str:
    variant = TIME_VARIANTS.get(time_of_day, TIME_VARIANTS["golden_hour"])
    return (
        f"{base_scene}, "
        f"{variant['lighting']}, "
        f"mood: {variant['mood']}, "
        f"color palette: {variant['color_palette']}, "
        f"{time_of_day} photography"
    )


if __name__ == "__main__":
    print("시간대별 여행 사진 비교 생성")
    print("=" * 40)

    for time_variant in ["golden_hour", "blue_hour"]:
        prompt = build_travel_prompt(BASE_SCENE, time_variant)
        output_path = f"outputs/travel_{time_variant}.png"
        print(f"\n[{time_variant}] 생성 중...")
        path = generate_image(prompt, output_path, model="dalle")
        print(f"  저장됨: {path}")

    print("\n완료! outputs/ 폴더에서 두 이미지를 비교해보세요.")
