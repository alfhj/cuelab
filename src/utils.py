import os
from pathlib import Path
import shutil
from config import BINARY_PATH, CUES_DIR, CUES_FILE
from . import lorem

BINARIES = {"ffmpeg": "", "mpv": ""}


def get_filelist() -> list[str]:
    cues_path = Path(CUES_DIR)
    cues_file_path = cues_path.joinpath(CUES_FILE)

    with open(cues_file_path, "r", encoding="utf-8") as f:
        contents = f.read().splitlines()

    return list(filter(lambda l: not (l.strip() == "" or l.startswith("#")), contents))
    # return [lorem.ipsum() for _ in range(100)]


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
