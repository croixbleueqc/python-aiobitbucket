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

from ...api import ApiBranchPagination, ApiLeaf

from ...typing.repositories import deploykey

class DeployKey(ApiLeaf,deploykey.DeployKey):
    """
    Manages SSH Keys

    https://developer.atlassian.com/bitbucket/api/2/reference/resource/repositories/%7Bworkspace%7D/%7Brepo_slug%7D/deploy-keys/%7Bkey_id%7D

    Coverage:
    - GET: Returns the deploy key belonging to a specific key.
    - POST: Create a new deploy key in a repository. (Delegate from DeployKeys)
    - PUT: Update a deploy key (WARNING: Seems not really supported despite documented on API 2.0)
    - DELETE: This deletes a deploy key from a repository.
    """
    def __init__(self, api_url, network, key_id=None, data=None, parent=None):
        ApiLeaf.__init__(self, api_url, network)
        deploykey.DeployKey.__init__(self, data=data, parent=parent)

        if key_id is not None:
            self.id = key_id
    
    def _generate_api_url(self):
        if self.id is None:
            return self._api_url
        else:
            return "{}/{}".format(
                self._api_url,
                self.id
            )

class DeployKeys(ApiBranchPagination):
    """
    https://developer.atlassian.com/bitbucket/api/2/reference/resource/repositories/{workspace}/{repo_slug}/deploy-keys

    Coverage:
    - GET: Returns all deploy-keys belonging to a repository.
    - POST: Delegate to DeployKey object
    """

    def __init__(self, api_url_reposlug, network):
        ApiBranchPagination.__init__(self, api_url_reposlug + "/deploy-keys", network, DeployKey)

    def by_key_id(self, key_id):
        return DeployKey(self._api_url, self._network, key_id=key_id)
