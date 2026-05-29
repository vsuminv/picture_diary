import os
from pathlib import Path
from openai import OpenAI
import requests
import  base64


STYLE_PREFIX = (
    "20대 여성, 중단발 머리, 따뜻한 미소, "
    "따뜻한 느낌의 수채화 일러스트 스타일"
)


def _save_b64_to_png(b64_data:str, save_path: Path) -> str:
    """URL에서 이미지를 다운로드하여 PNG로 저장합니다."""
    save_path.parent.mkdir(parents=True, exist_ok=True)
    save_path.write_bytes(base64.b64decode(b64_data))
    return str(save_path)


def generate_gpt(client:OpenAI, prompt:str, save_path:Path) -> str:
    """gpt-imageX 이미지를 생성하고 저장 경로를 반환합니다."""
    full_prompt = STYLE_PREFIX + prompt
    result = client.images.generate(
        model="gpt-image-1.5",
        prompt=full_prompt,
        size="1024x1024",
        quality="auto",
        n=1,
        output_format="png"
    )
    b64_data = result.data[0].b64_json
    return _save_b64_to_png(b64_data, save_path)

def generate_image(scene:dict, backend:str = "fal") -> str:
    """장면 한 항목을 받아 이미지를 생성한다. 경로 정보 반환
    ARGS:
      scenes : {"scene_id" : int, "scene_kr" : str, "prompt_en" : str}
      backend : "gpt" -> generate_gpt, "fal" -> generate_fal
      RETURN:
        저장된 이미지 파일의 경로
    """
    scene_id = scene.get("scene_id", 1)
    prompt = scene.get("prompt_en", "")
    save_path = Path("outputs")
    save_path = save_path / f"picture_diary_{scene_id}.png"
    print("이미지 생성 중....")
    
    if backend == "gpt":
        client = OpenAI()
        return generate_gpt(client, prompt, save_path)
    else:
        return(prompt, save_path)