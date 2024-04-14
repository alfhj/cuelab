from pathlib import Path
from rich.console import Console
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from readchar import readkey
from readchar import key as special_keys
from . import lorem

console = Console()


def make_layout() -> Layout:
    root = Layout(name="root")
    root.split_row(Layout(name="left"), Layout(name="right"))
    return root


def get_filelist(filename: str) -> list[str]:
    with open(filename, "r", encoding="utf-8") as f:
        contents = f.read().splitlines()
    
    return list(filter(lambda l: not(l.strip() == "" or l.startswith("#")), contents))
    #return [lorem.ipsum() for _ in range(100)]


def get_debug_panel(**kwargs):
    text = "\n".join(f"{key} = {value}" for key, value in kwargs.items())
    return Panel(text)


def get_book_variable_module_name(module_name):
    module = globals().get(module_name, None)
    book = {}
    if module:
        book = {key: value for key, value in module.__dict__.iteritems() if not (key.startswith("__") or key.startswith("_"))}
    return book


def get_visible_filelist(filelist: list[str], number_visible: int, selected_index: int, playing_index=None, middle_index: int = None) -> list[str]:
    """Gets the list of files which are visible within a certain number of lines

    Args:
        filelist (list[str]): complete list of filenames
        number_visible (int): number of files which are visible, usually around terminal height
        index (int): index of the file currently selected
        playing_index (int): index of the file currently playing. Defaults to index
        middle_index (int): index along the output where the currently selected file should appear. Defaults to number_visible // 2

    Returns:
        str: newline-separated string of filenames
    """

    if playing_index is None:
        playing_index = selected_index
    if middle_index is None:
        middle_index = number_visible // 2
    assert middle_index < number_visible

    from_index = max(selected_index - middle_index, 0)
    lines = filelist[from_index:]  # rich will take care of cutting off the rest
    local_selected_index = selected_index - from_index
    local_playing_index = playing_index - from_index
    for i in range(len(lines)):
        if i == local_playing_index:
            lines[i] = f"[bright_yellow]{lines[i]}[/]"
        elif i == local_selected_index:
            lines[i] = lines[i]
        else:
            lines[i] = f"[bright_black]{lines[i]}[/]"

    return "\n".join(lines), from_index, local_selected_index, local_playing_index


def handle_keypress():
    global selected_index
    global playing_index
    global max_index

    key = readkey()
   
    if key == special_keys.UP:
        selected_index = max(selected_index - 1, 0)
    if key == special_keys.DOWN:
        selected_index = min(selected_index + 1, max_index)
    if key == special_keys.SPACE:
        if selected_index != playing_index:
            playing_index = selected_index
        else:
            playing_index = min(playing_index + 1, max_index)
            selected_index = playing_index
    if key == "w" or key == "W":
        playing_index = max(playing_index - 1, 0)
    if key == "s" or key == "S":
        playing_index = min(playing_index + 1, max_index)

    return key


def update_view(live: Live, layout: Layout, pressed_key: bool = None):
    global filelist

    height = live.console.height - 2
    if pressed_key:
        pressed_key = next((k for k, v in special_keys.__dict__.items() if not pressed_key.startswith("_") and pressed_key == v), pressed_key)
    visible_filelist, i1, i2, i3 = get_visible_filelist(filelist, height, selected_index, playing_index)
    layout["left"].update(Panel(visible_filelist))
    layout["right"].update(get_debug_panel(key=pressed_key, selected_index=selected_index, playing_index=playing_index, fromi=i1, local_s=i2, local_p=i3, height=height))
    live.refresh()

def run(cues_dir, cues_file):
    global filelist
    global selected_index
    global playing_index
    global max_index
    
    cues_path = Path(cues_dir)
    cues_file_path = cues_path.joinpath(cues_file)
    filelist = get_filelist(str(cues_file_path))
    selected_index = 0
    playing_index = 0
    max_index = len(filelist) - 1
    layout = make_layout()

    with Live(layout, screen=True, auto_refresh=False) as live:
        update_view(live, layout)

        while True:
            key = handle_keypress()
            update_view(live, layout, key)
