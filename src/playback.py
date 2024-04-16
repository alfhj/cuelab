from io import StringIO
import logging
from rich.panel import Panel
from rich.text import Text
from python_mpv_jsonipc import MPV

from .constants import LOG_LEVEL_MAP

from .utils import BINARIES


def start_mpv(live, layout):
    log_stream = StringIO()
    handler = logging.StreamHandler(log_stream)
    mpv_logger = logging.getLogger("mpv")
    mpv_logger.addHandler(handler)

    def log_mpv(level, prefix, text):
        mpv_logger.log(LOG_LEVEL_MAP[level], text)  # f"{prefix}: {text}")
        lines = log_stream.getvalue().splitlines()
        text = Text("\n".join(lines[-live.console.height + 12 :]), overflow="crop", no_wrap=True)
        layout["lower"].update(Panel(text))

    extra_config = {"config": "no", "include": "bin/mpv.conf"}
    mpv = MPV(mpv_location=BINARIES["mpv"], loglevel="info", log_handler=log_mpv, **extra_config)
    mpv.set("fullscreen", "yes")  #  workaround for --fs --fs-screen=X not working

    return mpv, log_stream
