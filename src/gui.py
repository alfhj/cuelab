from dataclasses import dataclass

from rich.console import Console, ConsoleOptions, RenderResult

from .entities import Cue
from .utils import seconds_to_timestamp


@dataclass
class CueList:
    def __init__(self, cues: list[Cue], middle_position: float = 0.5):
        self.cues = cues
        self.middle_position = middle_position
        self.selected_index = 0
        self.playing_index = None
        self.max_index = len(self.cues) - 1
        self.current_seconds = 0

    def __rich_console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
        width, height = options.max_width, options.max_height
        middle_index = round(self.middle_position * height)

        from_index = max(self.selected_index - middle_index, 0)
        local_selected_index = self.selected_index - from_index
        local_playing_index = self.playing_index - from_index if self.playing_index is not None else None
        visible_cues = self.cues[from_index:]  # rich will take care of cutting off the rest
        lines = []

        for i, cue in enumerate(visible_cues):
            playing = False
            if local_playing_index is not None and i == local_playing_index:
                style = "bright_yellow"
                playing = True
            elif i == local_selected_index:
                style = None
            else:
                style = "grey50"

            cue_name = cue.name
            cue_info = f"{seconds_to_timestamp(cue.duration)} {cue.get_emoji()}"
            if playing:
                cue_info = f"{seconds_to_timestamp(self.current_seconds)} / {cue_info}"

            space = width - len(cue_info) - len(cue_name) - 1
            if space < 4:
                cue_name = cue_name[:space-4] + "..."
                space = 1

            line = cue_name + " "*space + cue_info
            if style:
                line = f"[{style}]{line}[/]"

            #lines.append(line)
            yield line

        #yield "\n".join(lines)

    def select_previous(self):
        self.selected_index = max(self.selected_index - 1, 0)

    def select_next(self):
        self.selected_index = min(self.selected_index + 1, self.max_index)

    def play_selected(self) -> Cue:
        self.playing_index = self.selected_index
        self.current_seconds = 0
        self.select_next()
        return self.cues[self.playing_index]

    def stop_playing(self):
        self.playing_index = None
        self.current_seconds = 0
