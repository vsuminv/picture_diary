import json
import os

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
      "scene_kr": "한국어로 장면을 묘사하는 설명 (50자 이내)",
      "prompt_en": "Detailed English image generation prompt for DALL-E (include lighting, mood, style, composition)"
    }
  ]
}

[장면 추출 원칙]
- 각 장면은 독립적으로 하나의 이미지로 표현 가능해야 합니다
- prompt_en은 여행 야경 사진 스타일로 구체적으로 작성하세요
- 조명(lighting), 분위기(mood), 시각적 초점(visual focus)을 반드시 포함하세요
- 텍스트, 워터마크, 흐릿한 요소는 제외 방향으로 작성하세요
"""


def extract_scenes(diary_text: str) -> list[dict]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY가 .env에 설정되지 않았습니다.")

    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"다음 여행 일기에서 장면을 추출해주세요:\n\n{diary_text}"},
        ],
        response_format={"type": "json_object"},
        temperature=0.7,
        max_tokens=1500,
    )

    content = response.choices[0].message.content
    data = json.loads(content)
    return data.get("scenes", [])
