"""The commands used within the application."""

##############################################################################
# Python imports.
from dataclasses import dataclass
from re import findall

##############################################################################
# Rich imports.
from rich.text import Text

##############################################################################
# Textual imports.
from textual.binding import Binding
from textual.message import Message

##############################################################################
# Local imports.
from ...raindrop import Collection, Tag


##############################################################################
class Command(Message):
    """Base class for all application command messages."""

    COMMAND: str | None = None
    """The text for the command.

    Notes:
        If no `COMMAND` is provided the class name will be used.
    """

    BINDING_KEY: str | None = None
    """The binding key for the command."""

    @classmethod
    def command(cls) -> str:
        """The text for the command.

        Returns:
            The command's textual name.
        """
        return cls.COMMAND or " ".join(findall("[A-Z][^A-Z]*", cls.__name__))

    @classmethod
    def tooltip(cls) -> str:
        """The tooltip for the command."""
        return cls.__doc__ or ""

    @classmethod
    def maybe_add_binding(cls, text: str | Text) -> Text:
        """Append the binding to the given text, if there is one.

        Args:
           text: The text to add the binding to.

        Returns:
            The text, with the binding added if there is one.
        """
        if isinstance(text, str):
            text = Text(text)
        if cls.BINDING_KEY:
            return text.append_text(Text(f" [{cls.BINDING_KEY}] ", style="dim"))
        return text

    @classmethod
    def binding(cls, action: str | None = None) -> Binding:
        """Create a binding object for the command.

        Args:
            action: The optional action to call for the binding.
        """
        if not cls.BINDING_KEY:
            raise ValueError("No binding key defined, unable to create a binding")
        return Binding(
            cls.BINDING_KEY,
            action or f"{cls.__name__.lower()}_command",
            description=cls.command(),
            tooltip=cls.tooltip(),
        )


##############################################################################
class SearchCollections(Command):
    """A message that requests the collection-based command palette is shown."""


##############################################################################
@dataclass
class ShowCollection(Command):
    """A message that requests that a particular collection is shown."""

    collection: Collection
    """The collection to show."""


##############################################################################
class SearchTags(Command):
    """A message that requests that the tag-based command palette is shown."""


##############################################################################
@dataclass
class ShowTagged(Command):
    """A message that requests that Raindrops with a particular tag are shown."""

    tag: Tag
    """The tag to show."""


##############################################################################
class Logout(Command):
    """Forget your API token and remove the local raindrop cache"""

    BINDING_KEY = "f12"


### commands.py ends here
