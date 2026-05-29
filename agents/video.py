from openai import OpenAI
import time
from pathlib import Path
import requests

client = OpenAI()


def load_images(image_dir: str = "outputs") -> list[str]:
    images = sorted(Path(image_dir).glob("picture_diary_*.png"))
    return [str(img) for img in images]


def pick_image(image_paths: list[str]) -> str:
    return image_paths[-1]


def generate_video(image_path: str, output_path: str) -> str:

    with open(image_path, "rb") as f:
        image_bytes = f.read()

    task = client.videos.generate(
        model="gpt-image-1.5",
        image=image_bytes,
        prompt="cinematic travel video, slow camera movement, emotional atmosphere"
    )

    task_id = task.id

    while True:
        result = client.videos.retrieve(task_id)

        if result.status == "completed":
            video_url = result.output[0].url
            break

        if result.status == "failed":
            raise RuntimeError("video generation failed")

        time.sleep(2)

    r = requests.get(video_url)

    Path(output_path).parent.mkdir(exist_ok=True, parents=True)

    with open(output_path, "wb") as f:
        f.write(r.content)

    return output_path


def save_video():
    images = load_images()
    image = pick_image(images)

    video = generate_video(image, "outputs/picture_diary.mp4")

    return {
        "images": images,
        "video": video
    }

