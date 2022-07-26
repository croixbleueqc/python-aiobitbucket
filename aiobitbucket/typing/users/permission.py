"""
Typing for Permissions

https://developer.atlassian.com/bitbucket/api/2/reference/resource/user/permissions/
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
from ..repositories.repository import Repository


class Permission(Typing2):
    """
    https://developer.atlassian.com/bitbucket/api/2/reference/resource/user/permissions/repositories
    """

    READ = "read"
    WRITE = "write"
    ADMIN = "admin"

    READ_CAPABILITIES = [READ, WRITE, ADMIN]
    WRITE_CAPABILITIES = [WRITE, ADMIN]

    permission = Field()
    repository = Field(instanciator=Repository)

    def has_write(self):
        return self.permission in Permission.WRITE_CAPABILITIES
