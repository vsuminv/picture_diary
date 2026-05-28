import os
from pathlib import Path

import requests
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


def _save_url_to_png(url: str, save_path: Path) -> str:
    """URL에서 이미지를 다운로드하여 PNG로 저장합니다."""
    save_path.parent.mkdir(parents=True, exist_ok=True)
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    save_path.write_bytes(response.content)
    return str(save_path)


def generate_image(prompt: str, output_path: str, model: str = "dalle") -> str:
    """이미지를 생성하고 저장된 경로를 반환합니다.

    Args:
        prompt: 영문 이미지 생성 프롬프트
        output_path: 저장할 파일 경로 (예: outputs/travel_1.png)
        model: 사용할 모델 ("dalle" | "flux")
    Returns:
        저장된 이미지 파일 경로 문자열
    """
    Path("outputs").mkdir(exist_ok=True)
    save_path = Path(output_path)

    if model == "flux":
        import fal_client
        result = fal_client.subscribe(
            "fal-ai/flux/schnell",
            arguments={
                "prompt": prompt,
                "num_images": 1,
                "image_size": "landscape_4_3",
                "num_inference_steps": 4,
            },
        )
        image_url = result["images"][0]["url"]
        return _save_url_to_png(image_url, save_path)

    # DALL-E 3 (기본값) — standard 품질, URL 다운로드 방식
    
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )
    image_url = response.data[0].url
    return _save_url_to_png(image_url, save_path)