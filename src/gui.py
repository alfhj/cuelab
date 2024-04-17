from dataclasses import dataclass
from rich.console import Console, ConsoleOptions, RenderResult
from .utils import log


@dataclass
class Filelist:
    def __rich_console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
        #log(options.)
        yield "asd"
