from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
import json
import base64

load_dotenv()
client = OpenAI()

Path("outputs").mkdir(exist_ok=True)
Path("domains").mkdir(exist_ok=True)

products: list[dict] = [
   {"name": "laptop","size": "large", "shape": "flat",   "desc": "4K OLED 디스플레이를 탑재한 초슬림 프리미엄 노트북"},
]

shot_map: dict[str, str] = {
    "small":  "extreme macro close-up shot",
    "medium": "product close-up shot",
    "large":  "three-quarter wide product shot",
}

angle_map: dict[str, str] = {
    "round":  "45-degree elevated angle",
    "square": "straight front-facing angle",
    "flat":   "top-down flat lay angle",
}

PROMPT_STYLE = {
    "shot": "close-up",
    "angle": "eye-level",
    "lighting": "studio lighting",
    "lens_or_style": "50mm macro lens",
    "mood": "clean, professional"
}

def build_product_prompt(desc: str,background: str = "clean white") -> str:
    """제품 설명 기반 이미지 프롬프트 생성"""

    return (
        f"Professional product photography of {desc}, "
        f"{background} background, "
        "studio lighting with soft shadows, "
        "sharp focus, "
        "high-end commercial catalog style, "
        "50mm macro lens, "
        "ultra detailed, "
        "8K resolution"
    )

def save_product_json(products: list[dict]) -> None:
    """과제 제출용 JSON 저장"""

    scenes = []

    for idx, product in enumerate(products, start=1):

        scene = {
            "id": f"scene_{idx:02d}",
            "diary_sentence": f"오늘 새 {product['name']} 제품을 확인했다.",
            "visual_focus": product["name"],
            "prompt_addons": [
                "product photography",
                "clean white background",
                "soft shadows"
            ],
            "negative_prompt": "text, watermark, blurry"
        }

        scenes.append(scene)

    data = {
        "domain": "product",
        "version": "day5",
        "prompt_style": PROMPT_STYLE,
        "scenes": scenes
    }

    with open(
        "domains/product_prompts.json",
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("JSON 저장 완료 -> domains/product_prompts.json")

def generate_product_image(
    prompt: str,
    output_path: str
) -> str:
    """OpenAI 제품 이미지 생성"""

    result = client.images.generate(
        model="gpt-image-1.5",
        prompt=prompt,
        size="1024x1024",
        quality="auto",
        n=1,
        output_format="png"
    )


    b64_data = result.data[0].b64_json

    return save_b64_image(
        b64_data,
        Path(output_path)
    )


def save_b64_image(
    b64_data: str,
    save_path: Path
) -> str:

    save_path.parent.mkdir(parents=True, exist_ok=True)

    save_path.write_bytes(
        base64.b64decode(b64_data)
    )

    return str(save_path)



    # 1. JSON 저장
    save_product_json(products)

    # 2. 이미지 생성
    for product in products:

        shot = shot_map[product["size"]]
        angle = angle_map[product["shape"]]

        prompt = build_product_prompt(
            desc=product["desc"],
            background="minimal white studio"
        )

        prompt += f", {shot}, {angle}"

        print(f"\n생성 중: {product['name']}")

        output_path = (
            f"outputs/product_{product['name']}.png"
        )

        image_path = generate_product_image(
            prompt=prompt,
            output_path=output_path
        )

        print(f"저장 완료: {image_path}")


if __name__ == "__main__":

    # JSON 저장
    save_product_json(products)

    # 이미지 생성
    for product in products:

        shot = shot_map[product["size"]]
        angle = angle_map[product["shape"]]

        prompt = build_product_prompt(
            desc=product["desc"],
            background="minimal white studio"
        )

        prompt += f", {shot}, {angle}"

        print(f"\n생성 중: {product['name']}")

        output_path = (
            f"outputs/product_{product['name']}.png"
        )

        image_path = generate_product_image(
            prompt=prompt,
            output_path=output_path
        )

        print(f"저장 완료: {image_path}")