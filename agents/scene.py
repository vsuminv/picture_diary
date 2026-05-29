import json
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

SYSTEM_PROMPT = """
당신은 여행 일기를 분석하여 그림일기용 장면을 추출하는 전문가입니다.
입력된 일기 텍스트에서 2~3개의 시각적으로 생생한 장면을 추출하세요.

반드시 아래 JSON 형식으로만 응답하세요:
{
  "scenes": [
    {
      "scene_id": 1,
      "scene_kr": "한국어 1줄 장면 설명",
      "prompt_en" : "영문 이미지 프롬프트 1줄",
    }
  ]
}

[추출 원칙]
- 각 장면은 독립적으로 하나의 이미지로 표현 가능해야 합니다
- prompt_en은 반드시 영어로 작성하고 wide shot/medium shot/close-up, eye-level/low/high angle, soft/rim/backlit lighting, watercolor diary illustration 스타일 포함합니다.
- 야경 여행 테마에 맞는 시각적 표현을 사용하세요
- scene_id는 1부터 시작하여 순차적으로 증가시킵니다.
"""


def extract_scenes(diary_text: str) -> list[dict]:
    """일기 텍스트를 받아 scenes 리스트를 반환합니다."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY가 .env에 없습니다.")
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": diary_text},
        ],
        response_format={"type": "json_object"},
        temperature=0.7,
        max_tokens=1000,
    )
    content = response.choices[0].message.content
    data = json.loads(content)
    return data["scenes"]


def validate_scenes(scenes: list[dict]) -> list[str]:
    """scenes 리스트가 필수 필드(scene_kr, prompt_en)를 충족하는지 검증합니다."""
    errors: list[str] = []
    required_fields = {"scene_kr", "prompt_en"}
    for i, scene in enumerate(scenes, start=1):
        missing = required_fields - scene.keys()
        if missing:
            errors.append(f"장면 {i} 필드 누락: {missing}")
    return errors


# def save_scenes(scenes: list[dict], out_path: str) -> None:
#     """scenes 리스트를 JSON 파일로 저장합니다."""
#     out = Path(out_path)
#     out.parent.mkdir(parents=True, exist_ok=True)
#     with open(out, "w", encoding="utf-8") as f:
#         json.dump({"scenes": scenes}, f, ensure_ascii=False, indent=2)