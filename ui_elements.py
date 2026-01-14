import time
from rich.console import Console
from rich.text import Text
from rich.theme import Theme
from pyfiglet import Figlet

game_theme = Theme({
    "danger": "bold red",
    "success": "bold green",
    "dialogue": "italic cyan",
    "loot": "bold yellow"
})
console = Console(theme=game_theme)

def slow_print(message, style=None):
    colored_text = Text.from_markup(message, style=style)
    for i in range(len(colored_text)):
        char = colored_text[i:i+1]
        console.print(char, end="")
        time.sleep(0.02)
    print()

def print_game_name(text, font="slant", color="loot"):
    f = Figlet(font=font)
    art = f.renderText(text)
    console.print(art, style=color, highlight=False)