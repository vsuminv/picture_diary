from pathlib import Path

from dotenv import load_dotenv

from agents.image import generate_image

load_dotenv()

Path("outputs").mkdir(exist_ok=True)

products: list[dict] = [
    {"name": "wireless_earbuds", "size": "small", "shape": "round", "desc": "premium wireless earbuds with noise cancellation"},
    {"name": "smartwatch", "size": "medium", "shape": "square", "desc": "sleek smartwatch with AMOLED display and health sensors"},
    {"name": "laptop", "size": "large", "shape": "flat", "desc": "ultra-thin laptop with 4K OLED display"},
]

shot_map: dict[str, str] = {
    "small": "extreme macro close-up shot",
    "medium": "product close-up shot",
    "large": "three-quarter wide product shot",
}

angle_map: dict[str, str] = {
    "round": "45-degree elevated angle",
    "square": "straight front-facing angle",
    "flat": "top-down flat lay angle",
}


def build_product_prompt(desc: str, background: str = "clean white") -> str:
    return (
        f"Professional product photography of {desc}, "
        f"{background} background, "
        "studio lighting with soft shadows, sharp focus, "
        "high-end commercial catalog style, 50mm macro lens, "
        "ultra detailed, 8K resolution"
    )


if __name__ == "__main__":
    for product in products:
        shot = shot_map[product["size"]]
        angle = angle_map[product["shape"]]
        prompt = build_product_prompt(product["desc"])
        prompt += f", {shot}, {angle}"
        output_path = f"outputs/product_{product['name']}.png"
        print(f"생성 중: {product['name']}")
        path = generate_image(prompt, output_path, model="dalle")
        print(f"  저장됨: {path}")
