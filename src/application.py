from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.columns import Columns
from rich.text import Text
from readchar import readkey
from readchar import key as special_keys

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


def get_visible_filelist(cues: list, width: int, number_visible: int, selected_index: int, playing_index=None, middle_index: int = None) -> list[str]:
    """Gets the list of files which are visible within a certain number of lines

    Args:
        cues (list): metadata for each cue
        width (int): horizontal width of the left panel
        number_visible (int): number of files which are visible, usually around terminal height
        index (int): index of the file currently selected
        playing_index (int): index of the file currently playing
        middle_index (int): index along the output where the currently selected file should appear. Defaults to number_visible // 2

    Returns:
        str: newline-separated string of filenames
    """

    if middle_index is None:
        middle_index = number_visible // 2
    assert middle_index < number_visible

    from_index = max(selected_index - middle_index, 0)
    local_selected_index = selected_index - from_index
    local_playing_index = playing_index - from_index if playing_index is not None else None
    visible_cues = cues[from_index:]  # rich will take care of cutting off the rest
    lines = Text()
    durations = Text(justify="right")
    for i in range(len(visible_cues)):
        if local_playing_index is not None and i == local_playing_index:
            style = "bright_yellow"
        elif i == local_selected_index:
            style = None
        else:
            style = "grey50"
        minutes, seconds = divmod(int(visible_cues[i]["duration"]), 60)
        lines.append(visible_cues[i]["name"] + "\n", style=style)
        durations.append(f"{minutes}:{seconds:02}\n", style=style)

    return lines, durations


def handle_keypress(mpv, cues):
    global selected_index
    global playing_index
    global max_index

    key = readkey()

    if key == special_keys.UP:
        selected_index = max(selected_index - 1, 0)

    if key == special_keys.DOWN:
        selected_index = min(selected_index + 1, max_index)

    if key == special_keys.SPACE:
        #if selected_index != playing_index:
        #    playing_index = selected_index
        #else:
        #    playing_index = min(playing_index + 1, max_index)
        #    selected_index = playing_index
        playing_index = selected_index
        selected_index = min(selected_index + 1, max_index)
        mpv.play(cues[playing_index]["path"])

    if key == special_keys.ESC:
        playing_index = None
        mpv.stop()

    if key == "f":
        mpv.cycle("fullscreen")

    if key in [str(i) for i in range(10)]:
        mpv.set("fullscreen", "no")
        mpv.set("fs-screen", key)
        mpv.set("fullscreen", "yes")

    return key


def update_layout(live: Live, layout: Layout, cues: list, pressed_key: bool = None):
    global filelist

    height = live.console.height - 2
    if pressed_key:
        pressed_key = next((k for k, v in special_keys.__dict__.items() if not pressed_key.startswith("_") and pressed_key == v), pressed_key)
    visible_filelist, visible_durations = get_visible_filelist(cues, 0, height, selected_index, playing_index)
    layout["left"].update(Panel(Columns([visible_filelist, visible_durations], expand=True)))
    layout["upper"].update(get_debug_panel(key=pressed_key, selected_index=selected_index, playing_index=playing_index, height=height))
    live.refresh()


def start(cues: list):
    global selected_index
    global playing_index
    global max_index
    global screen_number

    selected_index = 0
    playing_index = None
    max_index = len(cues) - 1
    screen_number = 0
    layout = make_layout()

    with Live(layout, screen=True, auto_refresh=True, refresh_per_second=4, vertical_overflow="crop") as live:
        update_layout(live, layout, cues)
        mpv, _ = start_mpv(live, layout)

        @ mpv.property_observer("eof-reached")
        def handle_eof(name, value):
            global playing_index
            if value == True:
                mpv.stop()
                playing_index = None
                update_layout(live, layout, cues)

        while True:
            try:
                key = handle_keypress(mpv, cues)
                update_layout(live, layout, cues, key)
            except KeyboardInterrupt:
                mpv.quit()
                quit()
