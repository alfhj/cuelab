import os
from pathlib import Path
import subprocess
from rich.panel import Panel
import time

from config import OUTPUT_DIR
from .utils import BINARIES
import prepare_cues 

__process = None

#class Player():
#    def __init__():


#mpv --keep-open=always --keep-open-pause=no --fullscreen --audio-display=external-first --script-opts=osc-visibility=always --playlist=cues.txt
def start_mpv(live, layout):
    playlist_file = Path(OUTPUT_DIR).joinpath("playlist.txt")
    if not playlist_file.is_file():
        raise FileNotFoundError(f"{playlist_file} not found. Make sure to run {prepare_cues.__name__}.py first")
    socket = r"\\.\pipe\mpvsocket" if os.name == "nt" else "/tmp/mpvsocket"
    command = [
        BINARIES["mpv"],
        "--no-config",
        "--include=bin/mpv.conf",
        "--input-ipc-server=" + socket,
        "--playlist=" + str(playlist_file)
    ]
    #layout["lower"].update(Panel(repr(command)))
    __process = subprocess.Popen(command, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = []
    for line in iter(__process.stdout.readline, b""):
        output.append(line.decode())
        layout["lower"].update(Panel("\n".join(output[-10:])))
        live.refresh()

    #stdout, stderr = __process.communicate()
    #layout["lower"].update(Panel(stdout.decode()))
    #live.refresh()

    time.sleep(10)