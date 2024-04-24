from readchar import key as special_keys
from readchar import readkey
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel

from config import CUE_LIST_MIDDLE, NUM_INSTANCES

from .gui import CueList
from .playback import start_mpv


def make_layout() -> Layout:
    root = Layout(name="root")
    root.split_row(Layout(name="left"), Layout(name="right"))
    root["right"].split_column(Layout(name="upper"), Layout(name="lower"))
    root["upper"].size = 10

    root["left"].update(Panel(""))
    root["upper"].update(Panel(""))
    root["lower"].update(Panel(""))

    return root


def get_debug_panel(**kwargs):
    text = "\n".join(f"{key} = {value}" for key, value in kwargs.items())
    return Panel(text)


def get_book_variable_module_name(module_name):
    module = globals().get(module_name, None)
    book = {}
    if module:
        book = {key: value for key, value in module.__dict__.iteritems() if not (key.startswith("__") or key.startswith("_"))}
    return book


def handle_keypress(mpv):
    global cue_list
    global screen_number
    global pressed_key

    key = readkey()
    pressed_key = next((k for k, v in special_keys.__dict__.items() if not key.startswith("_") and key == v), key)

    if key == special_keys.UP:
        cue_list.select_previous()

    if key == special_keys.DOWN:
        cue_list.select_next()

    if key == special_keys.SPACE:
        cue = cue_list.play_selected()
        mpv.play(cue.path)

    if key == special_keys.ESC:
        cue_list.stop_playing()
        mpv.stop()

    if key == "f":
        mpv.cycle("fullscreen")

    if key in [str(i) for i in range(10)]:
        mpv.set("fullscreen", "no")
        mpv.set("fs-screen", key)
        mpv.set("fullscreen", "yes")
        screen_number = int(key)

    return key


def update_layout(live: Live, layout: Layout, refresh: bool = True):
    global cue_list
    global screen_number
    global pressed_key

    layout["left"].update(Panel(cue_list))
    layout["upper"].update(get_debug_panel(key=pressed_key, selected_index=cue_list.selected_index, playing_index=cue_list.playing_index, screen_number=screen_number))
    if refresh:
        live.refresh()


def start(cues: list):
    global cue_list
    global screen_number
    global pressed_key

    cue_list = CueList(cues, middle_position=CUE_LIST_MIDDLE/100)
    screen_number = 0
    pressed_key = None
    layout = make_layout()

    with Live(layout, screen=True, auto_refresh=True, refresh_per_second=4, vertical_overflow="crop") as live:
        update_layout(live, layout)

        mpv_list = [start_mpv(live, layout) for _ in range(NUM_INSTANCES)]

        while True:
            try:
                key = handle_keypress(mpv)
                update_layout(live, layout, key)
            except KeyboardInterrupt:
                mpv.quit()
                quit()
