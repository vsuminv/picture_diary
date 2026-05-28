"""
여행 블로그 도메인 — golden_hour vs blue_hour 시간대 비교 이미지 생성
보너스: 시간대 변형 비교 구현
"""

from pathlib import Path

from dotenv import load_dotenv

from agents.image import generate_image

load_dotenv()

Path("outputs").mkdir(exist_ok=True)

TIME_VARIANTS: dict[str, dict] = {
    "golden_hour": {
        "lighting": "warm golden sunset light, amber glow, long soft shadows",
        "mood":     "warm, romantic, nostalgic, glowing",
        "palette":  "golden yellows, warm oranges, honey tones",
    },
    "blue_hour": {
        "lighting": "cool twilight blue light, city lights just switching on, dusk",
        "mood":     "serene, mysterious, ethereal, contemplative",
        "palette":  "deep indigo blues, cool purples, silver whites",
    },
}

BASE_SCENE: str = (
    "A scenic travel landscape of a coastal village, "
    "traditional architecture, boats in calm harbor, cobblestone streets, "
    "professional travel photography, ultra detailed, cinematic composition, 8K"
)


def build_travel_prompt(base_scene: str, time_of_day: str) -> str:
    """기본 장면과 시간대를 받아 이미지 생성 프롬프트를 반환합니다."""
    variant = TIME_VARIANTS.get(time_of_day, TIME_VARIANTS["golden_hour"])
    return (
        f"{base_scene}, "
        f"{variant['lighting']}, "
        f"mood: {variant['mood']}, "
        f"color palette: {variant['palette']}, "
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

    print("\n두 이미지를 비교해보세요:")
    print("  outputs/travel_golden_hour.png")
    print("  outputs/travel_blue_hour.png")
