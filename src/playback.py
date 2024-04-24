import logging
from io import StringIO

from python_mpv_jsonipc import MPV
from rich.panel import Panel
from rich.text import Text

from .constants import LOG_LEVEL_MAP
from .utils import BINARIES
from config import WARP_MODE, WARP_PARAMS


class MPVInstance:
    def __init__(self):
        self.instance: MPV = _start_mpv()
        self.playing_path: str = None
        self.position: int = None

        @self.instance.property_observer("eof-reached")
        def handle_eof(name, value):
            global cue_list
            if value == True:
                mpv.stop()
                cue_list.playing_index = None
                update_layout(live, layout)

        @mpv.property_observer("time-pos")
        def handle_eof(name, value):
            global cue_list
            new_position = int(value) if value else 0
            old_position = cue_list.current_seconds
            cue_list.current_seconds = new_position
            update_layout(live, layout, refresh=new_position != old_position)

    def stop(self):
        self.playing_path = None
        self.instance.stop()

    def play(self, path):
        self.playing_path = path
        self.instance.play(self.path)


class MPVDaemon:
    def __init__(self):
        self.instances: list[MPVInstance] = None

    def get_next_instance(self):
        return next(instance for instance in self.instances if instance.playing_path is not None)


def get_warp_params():
    if WARP_MODE == "none":
        return {}
    elif WARP_MODE == "rect":
        scale_x = scale_y = WARP_PARAMS[0]
        pan_x = pan_y = 1
        if len(WARP_PARAMS) > 1:
            scale_y = WARP_PARAMS[1]
        if len(WARP_PARAMS) > 2:
            pan_x = WARP_PARAMS[2]
        if len(WARP_PARAMS) > 3:
            pan_y = WARP_PARAMS[3]
        return {
            "video-scale-x": str(scale_x),
            "video-scale-y": str(scale_y),
            "video-pan-x": str(pan_x),
            "video-pan-y": str(pan_y)
        }
    elif WARP_MODE == "quad":
        raise NotImplementedError()
    else:
        raise ValueError(f"Warp mode {WARP_MODE} is incorrect")


def _start_mpv():
    log_stream = StringIO()
    handler = logging.StreamHandler(log_stream)
    mpv_logger = logging.getLogger("mpv")
    mpv_logger.addHandler(handler)

    def log_mpv(level, prefix, text):
        mpv_logger.log(LOG_LEVEL_MAP[level], text)  # f"{prefix}: {text}")
        lines = log_stream.getvalue().splitlines()
        text = Text("\n".join(lines[-height + 12:]), overflow="crop", no_wrap=True)
        layout["lower"].update(Panel(text))

    extra_config = {
        "config": "no",
        "include": "bin/mpv.conf",
        **get_warp_params()
    }
    mpv = MPV(mpv_location=BINARIES["mpv"], loglevel="info", log_handler=log_mpv, **extra_config)
    mpv.set("fullscreen", "yes")  #  workaround for --fs --fs-screen=X not working

    return mpv
