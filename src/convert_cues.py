from pathlib import Path
import shutil
from PIL import Image, ImageDraw, ImageFont

from config import CUES_DIR, OUTPUT_DIR, WIDTH, HEIGHT, FONT, FONT_SIZE, FONT_POSITION, LINE_SPACING
from .utils import generate_filename, get_filelist


def generate_text_image(text: str, output_path: str | Path):
    img = Image.new("RGB", (WIDTH, HEIGHT), color="black")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(FONT, FONT_SIZE)

    y_top = HEIGHT * FONT_POSITION / 100
    for i, line in enumerate(text.split("\\n")):
        x = (WIDTH - draw.textlength(line, font)) / 2
        y = y_top + i * FONT_SIZE * LINE_SPACING
        draw.text((x, y), line, fill="white", font=font)

    img.save(output_path)


def clean_output_dir(output_dir: str):
    if not output_dir.is_dir():
        print(f'Making output directory "{output_dir}"')
        output_dir.mkdir()
    else:
        print(f'Cleaning output directory "{output_dir}"')
        for file in output_dir.iterdir():
            if file.is_file():
                file.unlink()


def convert():
    output_dir = Path(OUTPUT_DIR)
    clean_output_dir(output_dir)

    print(f"Converting text cues to images")
    text_cues = [cue for cue in get_filelist() if cue.startswith('"')]
    for i, filename in enumerate(text_cues):
        print(f"{i+1} / {len(text_cues)}")
        text = filename[1:-1]
        output_path = output_dir.joinpath(generate_filename(i))
        generate_text_image(text, output_path)


def convert_and_copy():
    output_dir = Path(OUTPUT_DIR)
    clean_output_dir(output_dir)

    print(f'Copying files to "{output_dir}"')
    filelist = get_filelist()
    playlist = ""
    for i, filename in enumerate(filelist):
        print(f"{i+1} / {len(filelist)}")
        if filename.startswith('"'):  # subtitle
            text = filename[1:-1]
            output_path = output_dir.joinpath(generate_filename(i))
            generate_text_image(text, output_path)
        else:
            input_path = Path(CUES_DIR).joinpath(filename)
            if not input_path.is_file():
                raise FileNotFoundError(f'Cue {filename} not found in "{CUES_DIR}"')
            output_path = output_dir.joinpath(generate_filename(i, input_path.suffix))
            shutil.copy(input_path, output_path)

        playlist += str(output_path.name) + "\n"

    with open(output_dir.joinpath("playlist.txt"), "w", encoding="utf-8", newline="\n") as f:
        f.write(playlist)
