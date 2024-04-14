from pathlib import Path
import subprocess

from config import OUTPUT_DIR
from .utils import BINARIES
import prepare_cues 

__process = None

#mpv --keep-open=always --keep-open-pause=no --fullscreen --audio-display=external-first --script-opts=osc-visibility=always --playlist=cues.txt
def start_mpv():
    playlist_file = Path(OUTPUT_DIR).joinpath("playlist.txt")
    if not playlist_file.is_file():
        raise FileNotFoundError(f"{playlist_file} not found. Make sure to run {prepare_cues.__name__}.py first")
    command = [
        BINARIES["mpv"],
        "--keep-open=always",
        "--keep-open-pause=no",
        "--fullscreen",
        "--script-opts=osc-visibility=never",
        "--playlist=" + str(playlist_file)
    ]
    print(command)
    __process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = __process.communicate()

    print('STDOUT:', stdout)
    print('STDERR:', stderr)