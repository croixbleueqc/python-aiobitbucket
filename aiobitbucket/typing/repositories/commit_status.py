"""
Typing for status

https://developer.atlassian.com/bitbucket/api/2/reference/resource/repositories/%7Bworkspace%7D/%7Brepo_slug%7D/commit/%7Bcommit%7D/statuses/build/%7Bkey%7D

Note: for now there only build status , eventualy there might be more.
"""

# Copyright 2022 Croix Bleue du Québec

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


class State(Enum):
    INPROGRESS = "INPROGRESS"
    SUCCESSFUL = "SUCCESSFUL"
    FAILED = "FAILED"
    STOPPED = "STOPPED"

    def __str__(self):
        return self.value


class LinksHref(Typing2):
    href = Field()
    name = Field()


class Links(Typing2):
    commit = Field(instanciator=LinksHref)


class CommitStatus(Typing2):
    links = Field(instanciator=Links)
    uuid = Field()
    key = Field()
    name = Field()
    description = Field()
    state = Field().converter(loads=State, dumps=str)
    url = Field()
    created_on = Field()
    updated_on = Field()
