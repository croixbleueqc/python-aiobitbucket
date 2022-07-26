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
from ...typing import refs


class Branch(ApiLeaf, refs.Branch):
    """
    Manages Branch

    https://developer.atlassian.com/bitbucket/api/2/reference/resource/repositories/%7Bworkspace%7D/%7Brepo_slug%7D/refs/branches/%7Bname%7D

    Coverage:
    - GET: Returns a branch object within the specified repository.
    - POST: Creates a new branch in the specified repository. (Delegate from Branches)
    - DELETE: Delete a branch in the specified repository (The main branch is not allowed to be deleted).
    """

    def __init__(self, api_url, network, name=None, data=None, parent=None):
        ApiLeaf.__init__(self, api_url, network, api_unsupported=ApiLeaf.UPDATE)
        refs.Branch.__init__(self, data=data, parent=parent)

        if name is not None:
            self.name = name

    def _generate_api_url(self):
        if self.name is None:
            return self._api_url
        else:
            return "{}/{}".format(self._api_url, self.name)


class Branches(ApiBranchPagination):
    """
    https://developer.atlassian.com/bitbucket/api/2/reference/resource/repositories/%7Bworkspace%7D/%7Brepo_slug%7D/refs/branches

    Coverage:
    - GET: Returns a list of all open branches within the specified repository. Results will be in the order the source control manager returns them.
    - POST: Delegate to Branch object
    """

    def __init__(self, api_url_refs, network):
        ApiBranchPagination.__init__(self, api_url_refs + "/branches", network, Branch)

    def by_name(self, name):
        return Branch(self._api_url, self._network, name=name)


class Refs(object):
    def __init__(self, api_url_reposlug, network):
        self.branches = Branches(api_url_reposlug + "/refs", network)
