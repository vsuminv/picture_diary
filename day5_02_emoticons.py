"""
이모티콘 캐릭터 도메인 — 감정별 표현 딕셔너리로 이미지 생성
보너스: APPEARANCE(str), EMOTIONS(dict) 8개 항목
"""

from pathlib import Path

from dotenv import load_dotenv

from agents.image import generate_image

load_dotenv()

Path("outputs").mkdir(exist_ok=True)

APPEARANCE: str = (
    "A cute round emoji character, big expressive eyes, "
    "simple facial features, bright yellow color, "
    "clean white background, digital illustration, flat design, emoji art style"
)

EMOTIONS: dict[str, str] = {
    "happy":       "wide smile, rosy cheeks, sparkling crescent eyes, cheerful",
    "sad":         "downturned mouth, teary eyes, drooping eyebrows, blue tinge",
    "angry":       "furrowed brows, red face, clenched teeth, steam from head",
    "surprised":   "wide circle eyes, O-shaped mouth, raised eyebrows, shock lines",
    "laughing":    "eyes squeezed shut, huge grin, tears of joy streaming down",
    "wink":        "one eye closed playfully, smirk smile, thumbs up gesture",
    "embarrassed": "bright red blushing cheeks, awkward nervous smile, hand behind head",
    "cool":        "dark sunglasses, relaxed confident smile, finger guns gesture",
}


if __name__ == "__main__":
    for emotion, expression in EMOTIONS.items():
        prompt = f"{APPEARANCE}, {expression}, {emotion} mood"
        save_path = f"outputs/emoji_{emotion}.png"
        print(f"감정 생성 중: {emotion}")
        path = generate_image(prompt, save_path, model="dalle")
        print(f"  저장됨: {path}")
