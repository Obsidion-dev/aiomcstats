"""Main tests."""
import aiomcstats
import pytest


def test_version() -> None:
    """Mock version."""
    assert aiomcstats.__version__ == "0.1.3"


def test_author() -> None:
    """Test author."""
    assert aiomcstats.__author__ == "Leon Bowie"


def test_title() -> None:
    """Test title."""
    assert aiomcstats.__title__ == "aiomcstats"


def test_copyright() -> None:
    """Test copyright."""
    assert aiomcstats.__copyright__ == "Copyright 2020-2021 Leon Bowie"


def test_license() -> None:
    """Test license."""
    assert (
        aiomcstats.__license__
        == """Copyright (C) 2021 Leon Bowie

This program is free software: you can redistribute it
and/or modify it under the terms of the GNU General Public
License as published by the Free Software Foundation,
either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License a
long with this program. If not, see <https://www.gnu.org/licenses/>."""
    )
