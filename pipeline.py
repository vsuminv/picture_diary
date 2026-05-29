from pathlib import Path

from dotenv import load_dotenv

from agents.image import generate_image
from agents.scene import extract_scenes, validate_scenes
# from generate_domain_prompts import load_or_generate

load_dotenv()


# def _enrich_prompt(prompt_en: str, prompt_style: dict) -> str:
#     """도메인 prompt_style 키워드로 이미지 프롬프트를 강화합니다."""
#     style_parts = [v for v in prompt_style.values() if v]
#     return f"{prompt_en}, {', '.join(style_parts)}"


def picture_diary_pipeline(diary_text: str) -> dict:
    """일기 텍스트 → 장면 추출 → 이미지 생성 전체 파이프라인.

    Args:
        diary_text: 여행 일기 텍스트
    Returns:
        {"scenes": list[dict], "images": list[str]}
    """
    Path("outputs").mkdir(exist_ok=True)

    # 일기 → 장면 추출
    print("[1] 장면 추출 중...")
    scenes = extract_scenes(diary_text)

    errors = validate_scenes(scenes)
    if errors:
        for err in errors:
            print(f"  경고: {err}")
    # save_scenes(scenes, "outputs/scene_extracted.json")
    print(f"  -> {len(scenes)}개 장면 추출 완료")

    # 3. 이미지 생성
    print("[2] 이미지 생성 중...")
    images = [] 
    for scene in scenes: 
        image_path = generate_image( scene=scene, backend="gpt" ) 
        images.append(image_path)
        return { "scenes": scenes, "images": images, }
    # images: list[str] = [] 
    # for i, scene in enumerate(scenes, start=1): 
    #     print(f"[{i}/{len(scenes)}] {scene['scene_kr']}") 
    #     image_path = generate_image( scene=scene, backend="gpt" ) 
    #     images.append(image_path) 
    #     print(f"저장 완료: {image_path}") 
    #     return { "scenes": scenes, "images": images, }

if __name__ == "__main__":
    diary = (
        # "오늘 도쿄 시부야 교차로의 야경을 봤다. "
        # "형형색색의 네온사인이 밤하늘을 밝히고, 수많은 사람들이 교차로를 가득 메웠다. "
        # "멀리 도쿄 타워가 황금빛으로 빛나고 있었고, "
        # "강변에서 도시 불빛이 수면 위로 반사되는 모습에 한참을 넋을 잃었다."
        "오늘 한강 공원에 가서 라면을 먹었다."
        "해가 천천히 지면서 하늘이 주황빛과 분홍빛으로 물들었다."
        "강물 위로 노을이 반사되는 모습을 바라보며 한참 동안 멍하니 앉아 있었다."
        "선선한 바람과 함께 하루가 조용하게 마무리되는 기분이었다."
    )

    result = picture_diary_pipeline(diary)

    print(f"\n완료! 장면 {len(result['scenes'])}개 / 이미지 {len(result['images'])}개")
    for i, (scene, image_path) in enumerate( zip(result["scenes"], result["images"]), start=1 ): 
        print(f"\n[장면 {i}] {scene['scene_kr']}") 
        print(f" 이미지: {image_path}")
