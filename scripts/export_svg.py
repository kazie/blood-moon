import sys

from rich.ansi import AnsiDecoder
from rich.console import Console

console = Console(
    force_terminal=True, color_system="truecolor", highlight=True, record=True
)
decoder = AnsiDecoder()

data = sys.stdin.read()

for line in decoder.decode(data):
    console.print(line)

console.save_svg("help.svg")
