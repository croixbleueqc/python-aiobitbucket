"""
Typing for Repository

https://developer.atlassian.com/bitbucket/api/2/reference/resource/repositories/%7Bworkspace%7D/%7Brepo_slug%7D
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
from ..teams.projects import Project

from enum import Enum

class ForkPolicy(Enum):
    ALLOW_FORKS = "allow_forks"
    NO_PUBLIC_FORKS = "no_public_forks"
    NO_FORKS = "no_forks"

    def __str__(self):
        return self.value

class Scm(Enum):
    GIT = "git"
    HG = "hg"

    def __str__(self):
        return self.value

class LinksClone(Typing2):
    href = Field()
    name = Field()

class Links(Typing2):
    clone = Field().list_of(inside_instanciator=LinksClone)

    def find_clone_by_name(self, name):
        for i in self.clone:
            if i.name == name:
                return i

        return None

class Repository(Typing2):
    scm = Field(default=Scm.GIT) \
        .converter(loads=Scm, dumps=str)
    project = Field(instanciator=Project)
    is_private = Field(default=True)
    name = Field()
    description = Field()
    fork_policy = Field(default=ForkPolicy.NO_PUBLIC_FORKS) \
        .converter(loads=ForkPolicy, dumps=str)
    language = Field(default="")
    links = Field(instanciator=Links)


