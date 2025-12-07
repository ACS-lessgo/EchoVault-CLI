from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, VerticalScroll
from textual.widgets import Static , Footer , DataTable
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

# Dummy data for dev
DUMMY_TRACKS = [
    (1, "The Rolling Stones", "Paint It, Black", "Aftermath", 222),
    (2, "Queen", "Bohemian Rhapsody", "A Night at the Opera", 354),
    (3, "Daft Punk", "Get Lucky", "Random Access Memories", 276),
    (4, "Fleetwood Mac", "Dreams", "Rumours", 257),
    (5, "Tame Impala", "The Less I Know The Better The Less I Know The Better The Less I Know The Better The Less I Know The Better", "Currents", 217),
]

class EchoVault(App):
    CSS_PATH = "app.tcss"
    
    def compose(self) -> ComposeResult:
        with Container(id="app-grid"):
            # for displaying tracks
            with VerticalScroll(id="left-pane"):
                yield DataTable(id="track-table",show_cursor=True)
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
    
    # will be replaced by db call
    def load_track_data(self) -> None:
        table = self.query_one("#track-table", DataTable)
        
        table.add_columns("ID", "Artist", "Title", "Album", "Time")
        
        for track_id, artist, title, album, duration_seconds in DUMMY_TRACKS:
            minutes = int(duration_seconds // 60)
            seconds = int(duration_seconds % 60)
            formatted_duration = f"{minutes:02}:{seconds:02}"
            
            table.add_row(
                track_id, artist, title, album, formatted_duration, 
                key=f"track-{track_id}"
            )
            
    def load_stats(self) -> None:
        total_tracks = len(DUMMY_TRACKS)
        unique_artists = len({artist for _, artist, *_ in DUMMY_TRACKS})

        # compute total duration
        total_seconds = sum(t[-1] for t in DUMMY_TRACKS)
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        total_duration = f"{minutes:02}:{seconds:02}"

        # dummy values
        liked_songs = 12
        storage_used = "413 MB"
        folders = 8
        listening_time = "3h 12m"

        stats = {
            "Total Tracks": total_tracks,
            "Artists": unique_artists,
            "Liked Songs": liked_songs,
            "Storage Used": storage_used,
            "Folders": folders,
            "Total Duration": total_duration,
            "Listening Time": listening_time,
        }

        # get Static widgets under bottom-right
        bottom_widgets = self.query("#bottom-right > Static")

        for static in bottom_widgets:
            label_text = static.render().plain.strip()

            if label_text in stats:
                value = stats[label_text]
                static.update(f"{label_text}: [b]{value}[/b]")


        
    def on_mount(self) -> None:
        self.register_theme(arctic_theme) 
        self.register_theme(dracula_theme)
        self.theme = "arctic"
        
        # load tracks
        self.load_track_data()
        self.load_stats()
        
if __name__ == "__main__":
    app = EchoVault()
    app.run()