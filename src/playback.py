from io import StringIO
import logging
from rich.panel import Panel
from rich.text import Text
from python_mpv_jsonipc import MPV

from .utils import BINARIES

__process = None

#class Player():
#    def __init__():


#mpv --keep-open=always --keep-open-pause=no --fullscreen --audio-display=external-first --script-opts=osc-visibility=always --playlist=cues.txt
def start_mpv(live, layout):
    #playlist_file = Path(OUTPUT_DIR).joinpath("playlist.txt")
    #if not playlist_file.is_file():
    #    raise FileNotFoundError(f"{playlist_file} not found. Make sure to run {prepare_cues.__name__}.py first")
    #socket = r"\\.\pipe\mpvsocket" if os.name == "nt" else "/tmp/mpvsocket"
    #command = [
    #    BINARIES["mpv"],
    #    "--no-config",
    #    "--include=bin/mpv.conf",
    #    "--input-ipc-server=" + socket,
    #    "--playlist=" + str(playlist_file)
    #]
    ##layout["lower"].update(Panel(repr(command)))
    #__process = subprocess.Popen(command, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    #output = []
    #for line in iter(__process.stdout.readline, b""):
    #    output.append(line.decode())
    #    layout["lower"].update(Panel("\n".join(output[-10:])))
    #    live.refresh()

    #stdout, stderr = __process.communicate()
    #layout["lower"].update(Panel(stdout.decode()))
    #live.refresh()

    #mpv = MPV(mpv_location=BINARIES["mpv"], loglevel="info", log_handler=config="no", include="bin/mpv.conf")
    #for i in range(5, -1, -1):
    #    mpv.command("playlist_play_index", i)
    #    time.sleep(2)
    logging.basicConfig(filename="mpv.log", filemode="w", format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s", datefmt="%H:%M:%S", level=logging.DEBUG)
    log_stream = StringIO()
    handler = logging.StreamHandler(log_stream)
    mpv_logger = logging.getLogger("mpv-log")
    mpv_logger.addHandler(handler)
    log_level_map = {
        "fatal": logging.CRITICAL,
        "error": logging.ERROR,
        "warn": logging.WARNING,
        "info": logging.INFO,
        "v": logging.DEBUG,
        "debug": logging.DEBUG,
        "trace": logging.DEBUG,
    }
    
    def log_mpv(level, prefix, text):
        mpv_logger.log(log_level_map[level], text)#f"{prefix}: {text}")
        lines = log_stream.getvalue().splitlines()
        text = Text("\n".join(lines[-live.console.height+12:]), overflow="crop", no_wrap=True)
        layout["lower"].update(Panel(text))
    
    extra_config = {
        "config": "no",
        "include": "bin/mpv.conf"
    }
    mpv = MPV(mpv_location=BINARIES["mpv"], loglevel="info", log_handler=log_mpv, **extra_config)
    return mpv, log_stream