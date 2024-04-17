import json
from pathlib import Path
import shutil
import subprocess
from PIL import Image, ImageDraw, ImageFont
import hashlib

from config import CUES_DIR, CUES_FILE, METADATA_FILE, OUTPUT_DIR, WIDTH, HEIGHT, FONT, FONT_SIZE, FONT_POSITION, LINE_SPACING
from .entities import Cue, CueType
from .utils import BINARIES, dump_json, generate_filename, get_filelist, load_json, log


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
        log(f'Making output directory "{output_dir}"', __name__)
        output_dir.mkdir()
    else:
        log(f'Cleaning output directory "{output_dir}"', __name__)
        for file in output_dir.iterdir():
            if file.is_file():
                file.unlink()


def get_cues_hash():
    hash = hashlib.sha256()
    with open(CUES_FILE, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            hash.update(byte_block)
    return hash.hexdigest()


def get_media_info(file_path):
    command = [BINARIES["ffprobe"], "-v", "quiet", "-print_format", "json", "-show_streams", "-show_format", file_path]
    output = subprocess.check_output(command).decode("utf-8")
    info = json.loads(output)
    media_type = info["streams"][0]["codec_type"]
    media_length = float(info["format"]["duration"]) if "duration" in info["format"] else 0
    if media_type == "video" and media_length == 0:
        media_type = "image"

    return media_type, media_length


def convert() -> dict:
    metadata_file = Path(METADATA_FILE)
    output_dir = Path(OUTPUT_DIR)
    cues_hash = get_cues_hash()

    if metadata_file.is_file():
        metadata = load_json(metadata_file)
        if metadata["hash"] == cues_hash:
            log("Metadata is already up to date. Skipping generation of files.", __name__)
            return [Cue.fromJSON(obj) for obj in metadata["cues"]]

    clean_output_dir(output_dir)

    log(f'Generating metadata file "{output_dir}"', __name__)
    filelist = get_filelist()
    cues = []

    for i, filename in enumerate(filelist):
        log(f"Processing file {i+1} / {len(filelist)} ({filename})", __name__)
        if filename.startswith('"'):  # subtitle
            text = filename[1:-1]
            output_path = output_dir.joinpath(generate_filename(i))
            generate_text_image(text, output_path)
            cues.append(Cue(filename, CueType.TEXT, 0, str(output_path)))
        else:
            file_path = Path(CUES_DIR).joinpath(filename)
            if not file_path.is_file():
                raise FileNotFoundError(f'File "{filename}" was not found')
            media_type, media_duration = get_media_info(file_path)
            cues.append(Cue.fromJSON({
                "name": filename,
                "type": media_type,
                "duration": media_duration,
                "path": str(file_path)
            }))

    metadata = {
        "hash": cues_hash,
        "cues": [cue.toJSON() for cue in cues]
    }
    dump_json(metadata, metadata_file)

    return cues
