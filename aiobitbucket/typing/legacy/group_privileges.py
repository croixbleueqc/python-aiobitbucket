"""
Typing for Group Privileges
"""

# Copyright 2020 Croix Bleue du Québec

# This file is part of python-aiobitbucket.

# python-aiobitbucket is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# python-aiobitbucket is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License
# along with python-aiobitbucket.  If not, see <https://www.gnu.org/licenses/>.

from typing_engine.typing import Typing2, Field
from enum import Enum

class Privilege(Enum):
    """Supported privileges for a repository"""
    READ = "read"
    WRITE = "write"
    ADMIN = "admin"

    def __str__(self):
        return self.value

class GroupPrivilege(Typing2):
    """
    Privilege/group view
    """
    def __get_group_slug_only(self, value):
        if isinstance(value, dict):
            return value.get("slug")

        return value

    privilege = Field() \
        .converter(loads=Privilege, dumps=str)
    group = Field() \
        .getters(__get_group_slug_only)

class GroupPrivileges(Typing2):
    """Group all privilegies"""
    privileges = Field().list_of(GroupPrivilege)
