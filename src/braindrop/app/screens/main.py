"""The main screen for the application."""

##############################################################################
# Python imports.
from webbrowser import open as open_url

##############################################################################
# Textual imports.
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal
from textual.screen import Screen
from textual.widgets import Footer, Header, Placeholder

##############################################################################
# Local imports.
from ...raindrop import API
from ..widgets import Navigation


##############################################################################
class Main(Screen[None]):
    """The main screen of the application."""

    DEFAULT_CSS = """
    Header {
        /* The header icon is ugly and pointless. Remove it. */
        HeaderIcon {
            visibility: hidden;
        }

        /* The tall version of the header is utterly useless. Nuke that. */
        &.-tall {
            height: 1 !important;
        }
    }

    Navigation {
        width: 1fr;
    }

    Placeholder {
        width: 4fr;
    }
    """

    BINDINGS = [
        Binding("f2", "goto_raindrop", "raindrop.io"),
    ]

    def __init__(self, api: API) -> None:
        """Initialise the main screen.

        Args:
            api: The API client object.
        """
        super().__init__()
        self._api = api
        """The API client for Raindrop."""

    def compose(self) -> ComposeResult:
        """Compose the content of the screen."""
        yield Header()
        with Horizontal():
            yield Navigation(self._api)
            yield Placeholder()
        yield Footer()

    def action_goto_raindrop(self) -> None:
        """Open the Raindrop application in the browser."""
        open_url("https://app.raindrop.io/")


### main.py ends here
