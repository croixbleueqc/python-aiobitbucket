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

from ...api import ApiLeaf, ApiBranchPagination
from ...typing.repositories import pipeline


class PipelineUUID(ApiLeaf, pipeline.PipelineUUID):
    def __init__(self, api_url, network, id=None, data=None, parent=None):
        ApiLeaf.__init__(self, api_url, network)
        pipeline.PipelineUUID.__init__(self, data=data, parent=parent)

        if id is not None:
            self.id = id


class Pipelines(ApiBranchPagination):
    """
    Manages Pipelines

    https://developer.atlassian.com/bitbucket/api/2/reference/resource/repositories/%7Bworkspace%7D/%7Brepo_slug%7D/pipelines/


    """

    def __init__(self, api_url_reposlug, network):
        ApiBranchPagination.__init__(
            self, api_url_reposlug + "/pipelines/", network, PipelineUUID
        )
