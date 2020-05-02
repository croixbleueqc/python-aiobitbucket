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
from ...typing.repositories import branch_restrictions

class BranchRestriction(ApiLeaf, branch_restrictions.BranchRestriction):
    """
    Manages one branch restriction

    https://developer.atlassian.com/bitbucket/api/2/reference/resource/repositories/%7Bworkspace%7D/%7Brepo_slug%7D/branch-restrictions/%7Bid%7D

    Coverage:
    - GET: Returns a specific branch restriction rule.
    - POST: Creates a new branch restriction rule for a repository. (Delegate from BranchRestrictions)
    - PUT: Updates an existing branch restriction rule.
    - DELETE: Deletes an existing branch restriction rule.
    """
    def __init__(self, api_url, id=None, data=None, parent=None):
        ApiLeaf.__init__(self, api_url)
        branch_restrictions.BranchRestriction.__init__(self, data=data, parent=parent)

        if id is not None:
            self.id = id
    
    def _generate_api_url(self):
        if self.id is None:
            return self._api_url
        else:
            return "{}/{}".format(
                self._api_url,
                self.id
            )

class BranchRestrictions(ApiBranchPagination):
    """
    Manages branch restrictions

    https://developer.atlassian.com/bitbucket/api/2/reference/resource/repositories/{workspace}/{repo_slug}/branch-restrictions

    Coverage:
    - GET: Returns a paginated list of all branch restrictions on the repository.
    - POST: Delegate to BranchRestriction
    """
    def __init__(self, api_url_reposlug):
        ApiBranchPagination.__init__(self, api_url_reposlug + "/branch-restrictions", BranchRestriction)
    
    def by_id(self, id):
        return BranchRestriction(self._api_url, id=id)