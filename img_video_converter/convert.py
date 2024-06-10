import os
import time

from PIL import Image
from ffmpeg import FFmpeg
from pillow_heif import register_heif_opener

register_heif_opener()


def convert(filename, video=False, add_creation_time=False):
    base, old_ext = os.path.splitext(filename)
    ext = ".jpg" if not video else ".mp4"
    creation_time = os.path.getctime(filename)
    creation_time_human = time.strftime(
        "%Y-%m-%d_%H.%M.%S", time.localtime(creation_time)
    )
    print(f"Processing: {filename}, created at: {creation_time_human}")
    new_filename = (
        f"huttentocht 2022 yuv420p v2 {creation_time_human} {base}{ext}" if add_creation_time else f"{base}{ext}"
    )

    if os.path.exists(new_filename):
        print(f"File: {new_filename}, already exists. Skipped.")
        return

    if not video:
        img = Image.open(filename)
        try:
            img.save(new_filename)
        except OSError:  # cannot write mode RGBA as JPEG
            rgb_im = img.convert("RGB")
            rgb_im.save(new_filename)
    else:
        ffmpeg = (
            FFmpeg()
            .option("y")
            .input(filename)
            .output(
                new_filename,
                pix_fmt="yuv420p",
                vcodec="libx264",
                # vcodec="libx265",
                # vtag="hvc1",
            )
        )
        ffmpeg.execute()

    print("Created: " + new_filename)


if __name__ == "__main__":
    img_extensions = [".heic", ".HEIC", ".png", ".PNG", ".GIF", ".gif"]
    non_jpg_images = [
        f
        for f in os.listdir()
        if any(f.endswith(img_ext) for img_ext in img_extensions)
    ]

    video_extensions = [".avi", ".AVI", ".mts", ".m4v", ".MOV"]
    non_mp4_videos = [
        f
        for f in os.listdir()
        if any(f.endswith(vid_ext) for vid_ext in video_extensions)
    ]

    for x in non_jpg_images:
        convert(x)

    for x in non_mp4_videos:
        convert(x, video=True, add_creation_time=True)
