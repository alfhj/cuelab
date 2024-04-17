import json
import logging
import os
from pathlib import Path
import random
import shutil
from config import BINARY_DIR, CUES_FILE
from .entities import Cue
from . import lorem
import string

BINARIES = {"ffprobe": "", "mpv": ""}


def dump_json(obj, path, pretty=True):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=4 if pretty else None, ensure_ascii=False)


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def log(message, name=None):
    logging.getLogger("main").log(logging.INFO, message)


def generate_filename(i, ext=".png"):
    return str(i).zfill(5) + ext


def get_filelist() -> list[str]:
    cues_file_path = Path(CUES_FILE)

    with open(cues_file_path, "r", encoding="utf-8") as f:
        contents = f.read().splitlines()

    return list(filter(lambda l: not (l.strip() == "" or l.startswith("#")), contents))
    # return [lorem.ipsum() for _ in range(100)]


def get_binaries():
    files = os.listdir(BINARY_DIR)
    for binary in BINARIES:
        if local_file := next((f for f in files if f.startswith(binary) and os.access(f, os.X_OK)), None):
            BINARIES[binary] = local_file
            continue
        elif path_file := shutil.which(binary):
            BINARIES[binary] = path_file#.replace("COM", "EXE")
        else:
            raise FileNotFoundError(f'{binary} was not found in "{BINARY_DIR}" or PATH')


def generate_dummy_cues(n=100):
    return [Cue(
        name=lorem.ipsum(50),
        #name="".join(random.choice(string.ascii_letters) for _ in range(random.randint(40, 50))),
        type=random.choice(list(Cue.type_emoji_map.keys())),
        duration=random.randint(0, 120),
        path=""
    ) for _ in range(n)]
