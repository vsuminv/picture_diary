from pathlib import Path


def generate_video(image_path: str, output_path: str) -> str:
    """이미지를 받아 영상을 생성하고 저장된 경로를 반환합니다.

    Args:
        image_path: 입력 이미지 파일 경로
        output_path: 저장할 영상 파일 경로 (.mp4)
    Returns:
        저장된 영상 파일 경로 문자열
    """
    Path("outputs").mkdir(exist_ok=True)
    # 영상 생성은 fal-ai/kling 등으로 구현 예정
    return output_path
