"""
GPT-4o-mini를 사용해 도메인 프롬프트 JSON을 자동 생성하는 스크립트.
직접 실행: python generate_domain_prompts.py
pipeline.py 실행 시 domains/ 파일이 없으면 자동으로 호출됩니다.
"""

import json
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

DOMAIN_SCHEMAS: dict[str, str] = {
    "travel": """
여행 야경 도메인(travel night scenery)의 이미지 생성 프롬프트 설정 JSON을 만들어주세요.
주제: 여행 중 경험한 야경 — 도시 야경, 강변 야경, 별밤 하늘

반드시 아래 스키마를 정확히 따르세요:
{
  "domain": "travel",
  "version": "day5",
  "prompt_style": {
    "shot": "cinematic wide shot",
    "angle": "eye-level",
    "lighting": "city night lights and moonlight, long exposure glow",
    "lens_or_style": "24mm wide-angle lens, photorealistic 8K",
    "mood": "atmospheric, breathtaking, cinematic"
  },
  "scenes": [
    {
      "id": "scene_01",
      "diary_sentence": "한국어 일기 문장",
      "visual_focus": "시각적 초점 영문 1줄",
      "prompt_addons": ["키워드1", "키워드2", "키워드3"],
      "negative_prompt": "text, watermark, blurry, daytime"
    }
  ]
}

요구사항:
- prompt_style은 야경 촬영에 최적화된 전문 사진 용어 사용
- scenes는 정확히 3개: 도시 야경 / 강변 반사 / 별밤 마을
- prompt_addons는 각 장면마다 3~4개 키워드
- 영문 필드는 DALL-E 이미지 생성에 효과적인 표현으로 작성
""",
    "emoji": """
이모티콘 캐릭터 도메인의 이미지 생성 프롬프트 설정 JSON을 만들어주세요.
주제: 감정을 표현하는 귀여운 이모티콘 캐릭터

반드시 아래 스키마를 정확히 따르세요:
{
  "domain": "emoji",
  "version": "day5",
  "prompt_style": {
    "shot": "front-facing portrait",
    "angle": "straight-on",
    "lighting": "flat digital illustration lighting",
    "lens_or_style": "vector art, flat design, emoji style",
    "mood": "expressive, fun, colorful"
  },
  "scenes": [
    {
      "id": "scene_01",
      "diary_sentence": "한국어 일기 문장",
      "visual_focus": "시각적 초점 영문 1줄",
      "prompt_addons": ["키워드1", "키워드2", "키워드3"],
      "negative_prompt": "realistic, photo, dark, text"
    }
  ]
}

요구사항:
- scenes는 정확히 2개: 기쁨 / 놀람
- prompt_addons는 각 3~4개 키워드
""",
}


def generate_domain_config(domain: str) -> dict:
    """GPT-4o-mini로 지정 도메인의 프롬프트 설정 JSON을 생성합니다."""
    if domain not in DOMAIN_SCHEMAS:
        raise ValueError(f"지원하지 않는 도메인: {domain}. 가능한 값: {list(DOMAIN_SCHEMAS.keys())}")

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a professional prompt engineer for AI image generation.",
            },
            {"role": "user", "content": DOMAIN_SCHEMAS[domain]},
        ],
        response_format={"type": "json_object"},
        temperature=0.3,
        max_tokens=1000,
    )
    return json.loads(response.choices[0].message.content)


def save_domain_config(data: dict, domain: str) -> str:
    """도메인 설정 JSON을 domains/{domain}_prompts.json 으로 저장합니다."""
    out_dir = Path("domains")
    out_dir.mkdir(exist_ok=True)
    out_path = out_dir / f"{domain}_prompts.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return str(out_path)


def load_or_generate(domain: str = "travel") -> dict:
    """domains/{domain}_prompts.json 이 없으면 GPT로 생성, 있으면 로드합니다."""
    json_path = Path("domains") / f"{domain}_prompts.json"
    if json_path.exists():
        with open(json_path, "r", encoding="utf-8") as f:
            return json.load(f)

    print(f"[도메인 설정] {domain}_prompts.json 없음 → GPT-4o-mini로 생성 중...")
    data = generate_domain_config(domain)
    save_domain_config(data, domain)
    print(f"  -> 저장 완료: domains/{domain}_prompts.json")
    return data


if __name__ == "__main__":
    for domain in ["travel", "emoji"]:
        print(f"\n[{domain}] 도메인 프롬프트 JSON 생성 중...")
        data = generate_domain_config(domain)
        path = save_domain_config(data, domain)
        print(f"  저장 완료: {path}")
