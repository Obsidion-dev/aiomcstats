"""Aiomcstats.

An asyncronous minecraft server stats library
"""
#  Copyright (C) 2020 Leon Bowie
# This program is free software: you can redistribute it
# and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation,
# either version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License a
# long with this program. If not, see <https://www.gnu.org/licenses/>.

from importlib.metadata import version, PackageNotFoundError  # type: ignore

from .main import status
from .main import bedrock

try:
    __version__ = version(__name__)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"
__author__ = "Leon Bowie"
__copyright__ = "Copyright 2020-2021 Leon Bowie"
__title__ = "aiomcstats"
__license__ = """Copyright (C) 2021 Leon Bowie

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

__all__ = [
    "status",
    "bedrock",
]
