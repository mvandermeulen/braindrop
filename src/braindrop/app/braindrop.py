"""The main application class."""

##############################################################################
# Python imports.
import os

##############################################################################
# Textual imports.
from textual.app import App, InvalidThemeError
from textual.binding import Binding
from textual.widgets import HelpPanel

##############################################################################
# Local imports.
from ..raindrop import API
from .data import ExitState, load_configuration, save_configuration, token_file
from .screens import Main, TokenInput


##############################################################################
class Braindrop(App[ExitState]):
    """The Braindrop application class."""

    CSS = """
    /* Textual went to a full-width command palette and it looks like garbage.
       This makes it look less like it was unfinished and forgotten about. */
    CommandPalette > Vertical {
        width: 90%;
    }
    """

    BINDINGS = [
        Binding("ctrl+c, f10", "quit"),
        Binding("ctrl+p, super+x, :", "command_palette", "Commands", show=False),
        Binding(
            "f1, ?",
            "help",
            description="Help",
            tooltip="Toggle the display of the key binding help panel",
        ),
    ]

    def __init__(self) -> None:
        """Initialise the application."""
        super().__init__()
        configuration = load_configuration()
        if configuration.theme is not None:
            try:
                self.theme = configuration.theme
            except InvalidThemeError:
                pass

    def watch_theme(self) -> None:
        """Save the application's theme when it's changed."""
        configuration = load_configuration()
        configuration.theme = self.theme
        save_configuration(configuration)

    @staticmethod
    def environmental_token() -> str | None:
        """Try and get an API token from the environment.

        Returns:
           An API token found in the environment, or `None` if one wasn't found.
        """
        return os.environ.get("BRAINDROP_API_TOKEN")

    @property
    def api_token(self) -> str | None:
        """The API token for talking to Raindrop.

        If the token is found in the environment, it will be used. If not a
        saved token will be looked for and used. If one doesn't exist the
        value will be `None`.
        """
        try:
            return self.environmental_token() or token_file().read_text(
                encoding="utf-8"
            )
        except IOError:
            pass
        return None

    def token_bounce(self, token: str | None) -> None:
        """Handle the result of asking the user for their API token.

        Args:
            token: The resulting token.
        """
        if token:
            token_file().write_text(token, encoding="utf-8")
            self.push_screen(Main(API(token)))
        else:
            self.exit(ExitState.TOKEN_NEEDED)

    def on_mount(self) -> None:
        """Display the main screen.

        Note:
            If the Raindrop API token isn't known, the token input dialog
            will first be shown; the main screen will then only be shown
            once the token has been acquired.
        """
        if token := self.api_token:
            self.push_screen(Main(API(token)))
        else:
            self.push_screen(TokenInput(), callback=self.token_bounce)

    async def action_help(self) -> None:
        """Toggle the display of the help panel."""
        await self.run_action(
            f"{'hide' if self.screen.query(HelpPanel) else 'show'}_help_panel"
        )


### app.py ends here
