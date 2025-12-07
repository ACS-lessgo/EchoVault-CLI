from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, VerticalScroll
from textual.widgets import Static , Footer
from textual.theme import Theme
from rich.text import Text

dracula_theme = Theme(
    name="dracula",
    primary="#BD93F9",
    secondary="#6272A4",
    accent="#FF79C6",
    foreground="#F8F8F2",
    background="#282A36",
    panel="#1E1F29",
    surface="#3A3C4E",
    success="#50FA7B",
    warning="#F1FA8C",
    error="#FF5555",
    dark=True,
    variables={
        "block-cursor-text-style": "none",
        "footer-key-foreground": "#88C0D0",
        "input-selection-background": "#81a1c1 35%",
    },
)

arctic_theme = Theme(
    name="arctic",
    primary="#88C0D0",
    secondary="#81A1C1",
    accent="#B48EAD",
    foreground="#D8DEE9",
    background="#2E3440",
    success="#A3BE8C",
    warning="#EBCB8B",
    error="#BF616A",
    surface="#3B4252",
    panel="#434C5E",
    dark=True,
    variables={
        "block-cursor-text-style": "none",
        "footer-key-foreground": "#88C0D0",
        "input-selection-background": "#81a1c1 35%",
    },
)

class EchoVault(App):
    CSS_PATH = "app.tcss"
    
    def compose(self) -> ComposeResult:
        with Container(id="app-grid"):
            # for displaying tracks
            with VerticalScroll(id="left-pane"):
                for number in range(15):
                    yield Static(f"Track {number}")
            # app name        
            with Horizontal(id="top-right"):
                ECHO_ASCII = Text(
                    r"""
                ______     _            __     __          _ _    
                | ____|___| |__   ___   \ \   / /_ _ _   _| | |_  
                |  _| / __| '_ \ / _ \   \ \ / / _` | | | | | __| 
                | |__| (__| | | | (_) |   \ V / (_| | |_| | | |_  
                |_____\___|_| |_|\___/     \_/ \__,_|\__,_|_|\__|              
                """
                )
                ECHO_ASCII.stylize("bold")
                yield Static(ECHO_ASCII, id="logo")
            # for displaying user library information
            with Container(id="bottom-right"):
                yield Static("Total Tracks")
                yield Static("Artists")
                yield Static("Liked Songs")
                yield Static("Storage Used")
                yield Static("Folders")
                yield Static("Total Duration")
                yield Static("Listening Time", id="bottom-right-final")
        yield Footer()
        
    def on_mount(self) -> None:
        self.register_theme(arctic_theme) 
        self.register_theme(dracula_theme)
        self.theme = "arctic"
        
if __name__ == "__main__":
    app = EchoVault()
    app.run()