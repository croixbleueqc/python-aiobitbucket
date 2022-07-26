"""
Typing for Pipelines Config

https://developer.atlassian.com/bitbucket/api/2/reference/resource/repositories/%7Bworkspace%7D/%7Brepo_slug%7D/pipelines_config
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


class RepositoryPipelinesConfiguration(Typing2):
    enabled = Field(default=False)

    def __eq__(self, other):
        if not isinstance(other, RepositoryPipelinesConfiguration):
            return False
        return other.enabled == self.enabled


class StateResult(Typing2):
    name = Field()


class State(Typing2):
    name = Field()
    result = Field(instanciator=StateResult)


class Commit(Typing2):
    hash = Field()


class Target(Typing2):
    ref_type = Field()
    ref_name = Field()
    commit = Field(instanciator=Commit)


class PipelineUUID(Typing2):
    state = Field(instanciator=State)
    target = Field(instanciator=Target)
    build_number = Field()
