from pathlib import Path
import subprocess
import os
import shutil
import time
from PIL import Image, ImageDraw, ImageFont

from config import BINARY_PATH, CUES_DIR, OUTPUT_DIR, WIDTH, HEIGHT, FONT, FONT_SIZE, FONT_POSITION
from src.utils import get_filelist


BINARIES = {"ffmpeg": "", "mpv": ""}


def get_binaries():
    files = os.listdir(BINARY_PATH)
    for binary in BINARIES:
        if local_file := next((f for f in files if f.startswith(binary)), None):
            BINARIES[binary] = local_file
            continue
        elif path_file := shutil.which(binary):
            BINARIES[binary] = path_file
        else:
            raise FileNotFoundError(f'{binary} was not found in "{BINARY_PATH}" or PATH')


def generate_text_image(text: str, output_path: str | Path):
    img = Image.new("RGB", (WIDTH, HEIGHT), color="black")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(FONT, FONT_SIZE)
    x = (WIDTH - draw.textlength(text, font)) / 2
    y = (HEIGHT - FONT_SIZE) * (100 - FONT_POSITION) / 100
    draw.text((x, y), text, fill="white", font=font)
    img.save(output_path)
    # os.startfile("text_image.png")


def clean_output_dir(output_dir: Path):
    for file in output_dir.iterdir():
        if file.is_file():
            file.unlink()


if __name__ == "__main__":
    get_binaries()
    # print(BINARIES)

    output_dir = Path(OUTPUT_DIR)
    if not output_dir.is_dir():
        print(f'Making output directory "{output_dir}"')
        output_dir.mkdir()
    else:
        print(f'Cleaning output directory "{output_dir}"')
        clean_output_dir(output_dir)

    print(f'Copying files to "{output_dir}"')
    filelist = get_filelist()
    for i, filename in enumerate(filelist):
        print(f"{i+1} / {len(filelist)}")
        base = str(i).zfill(5)
        if filename.startswith('"'):  # subtitle
            text = filename[1:-1]
            output_path = output_dir.joinpath(base + ".png")
            generate_text_image(text, output_path)
        else:
            input_path = Path(CUES_DIR).joinpath(filename)
            if not input_path.is_file():
                raise FileNotFoundError(f'Cue {filename} not found in "{CUES_DIR}"')
            output_path = output_dir.joinpath(base + input_path.suffix)
            shutil.copy(input_path, output_path)
