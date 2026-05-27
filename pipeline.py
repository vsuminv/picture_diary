from pathlib import Path

from dotenv import load_dotenv

from agents.image import generate_image
from agents.scene import extract_scenes

load_dotenv()


def picture_diary_pipeline(diary_text: str) -> dict:
    Path("outputs").mkdir(exist_ok=True)

    scenes = extract_scenes(diary_text)
    images: list[str] = []

    for i, scene in enumerate(scenes):
        output_path = f"outputs/travel_{i + 1}.png"
        image_path = generate_image(scene["prompt_en"], output_path, model="dalle")
        images.append(image_path)

    return {
        "scenes": scenes,
        "images": images,
    }


if __name__ == "__main__":
    diary = (
        "오늘 도쿄 시부야 교차로의 야경을 봤다. "
        "형형색색의 네온사인이 밤하늘을 밝히고, 수많은 사람들이 교차로를 가득 메웠다. "
        "멀리 도쿄 타워가 황금빛으로 빛나고 있었고, "
        "강변에 서서 도시 불빛이 수면 위로 반사되는 모습에 한참을 넋을 잃었다."
    )

    result = picture_diary_pipeline(diary)
    print(f"추출된 장면: {len(result['scenes'])}개")
    print(f"생성된 이미지: {len(result['images'])}개")
    for i, scene in enumerate(result["scenes"]):
        print(f"\n[장면 {i + 1}]")
        print(f"  한국어: {scene['scene_kr']}")
        print(f"  프롬프트: {scene['prompt_en']}")
        print(f"  이미지: {result['images'][i]}")
