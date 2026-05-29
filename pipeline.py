from pathlib import Path

from dotenv import load_dotenv

from agents.image import generate_image
from agents.scene import extract_scenes, validate_scenes
from agents.video import save_video

load_dotenv()


def picture_diary_pipeline(diary_text: str) -> dict:
    """일기 텍스트 → 장면 추출 → 이미지 생성 → 영상 생성
    Args:
        diary_text: 그림 일기 텍스트
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
    print(f"  -> {len(scenes)}개 장면 추출 완료")

    # 3. 이미지 생성
    print("[2] 이미지 생성 중...")
    images: list[str] = []

    for i, scene in enumerate(scenes, start=1):
        print(f"[{i}/{len(scenes)}] {scene['scene_kr']}")

        image_path = generate_image(
            scene=scene,
            backend="gpt"
        )

        images.append(image_path)

        print(f"저장 완료: {image_path}")
    print("[3] 영상 생성 중...")

    video_result = save_video()

    print(f"영상 저장 완료: {video_result['video']}")

    return {
        "scenes": scenes,
        "images": images,
        "video": video_result["video"],
    }


if __name__ == "__main__":
    diary = (
        "오늘 한강 공원에 갔다."
        "해가 천천히 지면서 하늘이 주황빛과 분홍빛으로 물들었다."
        "강물 위로 노을이 반사되는 모습을 바라보며 한참 동안 멍하니 앉아 있었다."
        "선선한 바람과 함께 하루가 조용하게 마무리되는 기분이었다."
    )

    result = picture_diary_pipeline(diary)

    print(f"\n완료! 장면 {len(result['scenes'])}개 / 이미지 {len(result['images'])}개")
    for i, (scene, image_path) in enumerate( zip(result["scenes"], result["images"]), start=1 ): 
        print(f"\n[장면 {i}] {scene['scene_kr']}") 
        print(f" 이미지: {image_path}")
