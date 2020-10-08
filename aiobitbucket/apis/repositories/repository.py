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

from ...typing.repositories import repository

from .pipelines_config import PipelinesConfig
from .deploykeys import DeployKeys
from .branch_restrictions import BranchRestrictions
from ..legacy.group_privileges import GroupPrivilegesRepoSlug
from .pipelines import Pipelines
from .refs import Refs
from .src import Src
from .pullrequests import PullRequests

class RepoSlug(ApiLeaf, repository.Repository):
    """
    Manages repository

    https://developer.atlassian.com/bitbucket/api/2/reference/resource/repositories/%7Bworkspace%7D/%7Brepo_slug%7D

    Coverage:
    - GET: Returns the object describing this repository.
    - POST: Creates a new repository.
    - PUT: Update a repository
    - DELETE: Deletes the repository. This is an irreversible operation.
    """
    def __init__(self, network, workspace_name, repo_slug_name, data=None, parent=None):
        ApiLeaf.__init__(self, f"/2.0/repositories/{workspace_name}/{repo_slug_name}", network)
        repository.Repository.__init__(self, data=data, parent=parent)
        self._workspace_name = workspace_name
        self._repo_slug_name = repo_slug_name

    def pipelines_config(self):
        """Pipelines config API accessor"""
        return PipelinesConfig(self._api_url, self._network)

    def deploy_keys(self):
        """Deploy Keys API accessor"""
        return DeployKeys(self._api_url, self._network)

    def branch_restrictions(self):
        """Branch restrictions API accessor"""
        return BranchRestrictions(self._api_url, self._network)
    
    def group_privileges(self):
        """Group Privileges API accessor"""
        return GroupPrivilegesRepoSlug(self._network, self._workspace_name, self._repo_slug_name)

    def pipelines(self):
        """Find Pipelines accessor"""
        return Pipelines(self._api_url, self._network)
    
    def refs(self):
        """Branches and tags accessor"""
        return Refs(self._api_url, self._network)
    
    def src(self):
        """Source files accessor"""
        return Src(self._api_url, self._network)

    def pullrequests(self):
        """Pull Requests accessor"""
        return PullRequests(self._api_url, self._network)
