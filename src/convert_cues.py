import json
from pathlib import Path
import shutil
import subprocess
from PIL import Image, ImageDraw, ImageFont
import hashlib

from config import CUES_DIR, CUES_FILE, METADATA_FILE, OUTPUT_DIR, WIDTH, HEIGHT, FONT, FONT_SIZE, FONT_POSITION, LINE_SPACING
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


def convert_text():
    output_dir = Path(OUTPUT_DIR)
    clean_output_dir(output_dir)

    log(f"Converting text cues to images", __name__)
    text_cues = [cue for cue in get_filelist() if cue.startswith('"')]
    for i, filename in enumerate(text_cues):
        log(f"{i+1} / {len(text_cues)}", __name__)
        text = filename[1:-1]
        output_path = output_dir.joinpath(generate_filename(i))
        generate_text_image(text, output_path)


def convert_and_copy():
    output_dir = Path(OUTPUT_DIR)
    clean_output_dir(output_dir)

    log(f'Copying files to "{output_dir}"', __name__)
    filelist = get_filelist()
    playlist = ""
    for i, filename in enumerate(filelist):
        log(f"{i+1} / {len(filelist)}", __name__)
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


def metadata_is_updated(metadata: dict):
    return metadata["hash"] == get_cues_hash()


#def generate_metadata(metadata_file: Path):


def convert() -> dict:
    """ Converts text cues and generates a metadata file for all cues containing the following information:
    - Type of cue
    - Duration of cue for audio and video cues in seconds (0=inf)
    - Path of cue media, relative to CUES_DIR
        - For text cues: which PNG file in OUTPUT_DIR that corresponds to the cue
    Example:
    {
        "hash": "1a2b3c4d",
        "cues": [
            {
                "name": "babyshark.mp3",
                "type": "audio",
                "duration": 92,
                "path": "cues/babyshark.mp3"
            }
        ]
    }
    """
    metadata_file = Path(METADATA_FILE)
    output_dir = Path(OUTPUT_DIR)
    cues_hash = get_cues_hash()

    if metadata_file.is_file():
        metadata = load_json(metadata_file)
        if metadata["hash"] == cues_hash:
            log("Metadata is already up to date. Skipping generation of files.", __name__)
            return metadata

    clean_output_dir(output_dir)

    log(f'Generating metadata file "{output_dir}"', __name__)
    filelist = get_filelist()
    metadata = {
        "hash": cues_hash,
        "cues": []
    }

    for i, filename in enumerate(filelist):
        log(f"Processing file {i+1} / {len(filelist)} ({filename})", __name__)
        if filename.startswith('"'):  # subtitle
            text = filename[1:-1]
            output_path = output_dir.joinpath(generate_filename(i))
            generate_text_image(text, output_path)
            metadata["cues"].append({
                "name": filename,
                "type": "text",
                "duration": 0,
                "path": str(output_path)
            })
        else:
            file_path = Path(CUES_DIR).joinpath(filename)
            if not file_path.is_file():
                raise FileNotFoundError(f'File "{filename}" was not found')
            media_type, media_duration = get_media_info(file_path)
            metadata["cues"].append({
                "name": filename,
                "type": media_type,
                "duration": media_duration,
                "path": str(file_path)
            })

    dump_json(metadata, metadata_file)
    return metadata
