"""
Typing for Pull Requests

https://developer.atlassian.com/bitbucket/api/2/reference/resource/repositories/{workspace}/{repo_slug}/pullrequests
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


class State(Enum):
    MERGED = "MERGED"
    SUPERSEDED = "SUPERSEDED"
    OPEN = "OPEN"
    DECLINED = "DECLINED"

    def __str__(self):
        return self.value


class Branch(Typing2):
    name = Field()


class SrcDst(Typing2):
    branch = Field(instanciator=Branch)


class LinksHref(Typing2):
    href = Field()


class Links(Typing2):
    html = Field(instanciator=LinksHref)


class PullRequest(Typing2):
    title = Field()
    id = Field()
    close_source_branch = Field().converter(loads=bool)
    source = Field(instanciator=SrcDst)
    destination = Field(instanciator=SrcDst)
    state = Field().converter(loads=State, dumps=str)
    links = Field(instanciator=Links)
