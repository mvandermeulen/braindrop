"""Classes for holding collection information."""

##############################################################################
# Backward compatibility.
from __future__ import annotations

##############################################################################
# Python imports.
from dataclasses import dataclass
from datetime import datetime
from enum import IntEnum
from typing import Any

##############################################################################
# Local imports.
from .time_tools import get_time


##############################################################################
@dataclass(frozen=True)
class Collection:
    """Class that holds the details of a collection."""

    raw: dict[str, Any]
    """The raw data."""
    identity: int
    """The ID of the collection."""
    # access
    # collaborators
    color: str
    """The colour for the collection."""
    count: int
    """The number of items in the collection."""
    cover: list[str]
    """Cover images for the collection."""
    created: datetime | None
    """When the collection was created."""
    expanded: bool
    """Is the collection expanded?"""
    last_update: datetime | None
    """When the collection was last updated."""
    public: bool
    """Is the collection visible to the public?"""
    sort: int
    """The sort value for the collection."""
    title: str
    """The title of the collection."""
    # user
    view: str
    """The view method for the collection."""
    parent: int | None
    """The ID of the parent collection, if there is one."""

    @staticmethod
    def from_json(data: dict[str, Any]) -> Collection:
        """Create a collection from JSON-sourced data.

        Args:
            data: The data to create the object from.

        Returns:
            A fresh `Collection` instance.
        """
        return Collection(
            raw=data,
            identity=data["_id"],
            color=data.get("color", ""),
            count=data.get("count", 0),
            cover=data.get("cover", []),
            created=get_time(data, "created"),
            expanded=data.get("expanded", False),
            last_update=get_time(data, "lastUpdate"),
            public=data.get("public", False),
            sort=data.get("sort", 0),
            title=data.get("title", ""),
            view=data.get("view", ""),
            parent=data.get("parent", {}).get("$id"),
        )


##############################################################################
class SpecialCollection(IntEnum):
    """IDs of the special collections."""

    ALL = 0
    """A collection that contains all non-trashed raindrops."""
    UNSORTED = -1
    """A collection that contains all non-trashed raindrops that haven't been sorted."""
    TRASH = -99
    """A collection that contains all trashed raindrops."""
    UNTAGGED = -998
    """A collection that contains all untagged raindrops."""
    BROKEN = -999
    """A collection that contains all broken raindrops.

    Note:
        Unlike the other special collection IDs defined here, the broken
        collection isn't one that is supported via the API; but it's
        available here so that it can be treated as just another
        collection, with special handling within the main application.
    """

    def __call__(self) -> Collection:
        """Turn a collection ID into a `Collection` object."""
        return Collection(
            raw={},
            identity=self.value,
            color="",
            count=0,
            cover=[],
            created=None,
            expanded=True,
            last_update=None,
            public=False,
            sort=0,
            title=self.name.title(),
            view="",
            parent=-1,
        )


### collection.py ends here
