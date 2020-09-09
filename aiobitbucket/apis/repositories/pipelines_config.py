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

from ...api import ApiLeaf

from ...typing.repositories import pipeline

class PipelinesConfig(ApiLeaf, pipeline.RepositoryPipelinesConfiguration):
    """
    Manage Pipelines Configuation

    https://developer.atlassian.com/bitbucket/api/2/reference/resource/repositories/%7Bworkspace%7D/%7Brepo_slug%7D/pipelines_config

    Coverage:
    - GET: Retrieve the repository pipelines configuration.
    - PUT: Update the pipelines configuration for a repository.
    """
    def __init__(self, api_url_reposlug, network, data=None, parent=None):
        ApiLeaf.__init__(self, api_url_reposlug + "/pipelines_config", network, ApiLeaf.DELETE | ApiLeaf.CREATE)
        pipeline.RepositoryPipelinesConfiguration.__init__(self, data=data, parent=parent)

    async def enable(self):
        """Enable pipelines
        
        Get previous state and update it.
        """
        await self.get()

        if self.enabled != True:
            self.enabled = True
            await self.update()

    async def disable(self):
        """Disable pipelines
        
        Get previous state and update it.
        """
        await self.get()

        if self.enabled != False:
            self.enabled = False
            await self.update()
