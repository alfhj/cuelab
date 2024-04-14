from pathlib import Path
from config import CUES_DIR, CUES_FILE
from . import lorem


def get_filelist() -> list[str]:
    cues_path = Path(CUES_DIR)
    cues_file_path = cues_path.joinpath(CUES_FILE)

    with open(cues_file_path, "r", encoding="utf-8") as f:
        contents = f.read().splitlines()

    return list(filter(lambda l: not (l.strip() == "" or l.startswith("#")), contents))
    # return [lorem.ipsum() for _ in range(100)]
