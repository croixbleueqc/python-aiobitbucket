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
from ...typing.repositories import pullrequests


class PullRequest(ApiLeaf, pullrequests.PullRequest):
    """
    Manages Pull Request

    https://developer.atlassian.com/bitbucket/api/2/reference/resource/repositories/%7Bworkspace%7D/%7Brepo_slug%7D/pullrequests/%7Bpull_request_id%7D

    Coverage:
    - GET: Returns the specified pull request.
    - UPDATE: Mutates the specified pull request.
    - POST: Creates a new pull request where the destination repository is this repository and the author is the authenticated user. (Delegate from PullRequests)
    """

    def __init__(self, api_url, network, id=None, data=None, parent=None):
        ApiLeaf.__init__(self, api_url, network, api_unsupported=ApiLeaf.DELETE)
        pullrequests.PullRequest.__init__(self, data=data, parent=parent)

        if id is not None:
            self.id = id

    def _generate_api_url(self):
        if self.id is None:
            return self._api_url
        else:
            return "{}/{}".format(self._api_url, self.id)


class PullRequests(ApiBranchPagination):
    """
    https://developer.atlassian.com/bitbucket/api/2/reference/resource/repositories/%7Bworkspace%7D/%7Brepo_slug%7D/pullrequests

    Coverage:
    - GET: Returns all pull requests on the specified repository.
    - POST: Delegate to PullRequest object
    """

    def __init__(self, api_url_refs, network):
        ApiBranchPagination.__init__(
            self, api_url_refs + "/pullrequests", network, PullRequest
        )

    def get(self, filter=None):
        """Override the ApiBranchPagination.get

        Pagination for this API does not support pagelen as expected
        status=400, payload={'type': 'error', 'error': {'message': 'Invalid pagelen'}}
        """
        return ApiBranchPagination.get(self, filter=filter, pagelen=None)

    def by_id(self, id):
        return PullRequest(self._api_url, self._network, id=id)
