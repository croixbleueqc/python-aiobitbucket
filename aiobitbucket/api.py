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


from .errors import ApiUnsupported
from .network import Network, NetworkPagination
from .settings import Settings

"""
Define base class to implement 2.0 API endpoints.

endpoints are structured as /2.0/<branch>/<branch>/.../<leaf>

Important: ApiLeaf and ApiBranchPagination are maybe not enough to cover 100% of bitbucket API cases.
"""

class ApiLeaf(object):
    """
    A typical Leaf endpoint on 2.0 API.
    Most of the time, CREATE (POST) is delegate from a branch (an intermediate path)

    A Leaf is abstract and should be used with a Typing2 object
    """
    GET = 1 << 0
    UPDATE = 1 << 1
    DELETE = 1 << 2
    CREATE = 1 << 3

    def __init__(self, api_url, api_unsupported=0):
        self._api_url = api_url
        self._api_unsupported = api_unsupported

    def _generate_api_url(self):
        return self._api_url

    async def get(self):
        """
        GET
        """
        if self._api_unsupported & ApiLeaf.GET > 0:
            raise ApiUnsupported("GET")

        state = await Network.get(self._generate_api_url())
        self.loads_from_dict(state)
    
    async def update(self):
        """
        PUT
        """
        if self._api_unsupported & ApiLeaf.UPDATE > 0:
            raise ApiUnsupported("PUT")

        await Network.put(
            self._generate_api_url(),
            self.dumps()
        )

    async def delete(self):
        """
        DELETE
        """
        if self._api_unsupported & ApiLeaf.DELETE > 0:
            raise ApiUnsupported("DELETE")

        await Network.delete(self._generate_api_url())

    async def create(self):
        """
        POST

        Most of the time a delegate from a branch endpoints
        """
        if self._api_unsupported & ApiLeaf.CREATE > 0:
            raise ApiUnsupported("POST")

        result = await Network.post(
            self._api_url,
            self.dumps()
        )

        self.loads_from_dict(result)

class ApiBranchPagination(object):
    """
    A typical Branch in an endpoints

    Most of the time cast_leaf should be derived from ApiLeaf (see Warning on top)
    """
    NEW = 1 << 0

    def __init__(self, api_url, cast_leaf, api_unsupported=0):
        self._api_url = api_url
        self._cast_leaf = cast_leaf
        self._api_unsupported = api_unsupported
    
    def get(self, filter=None, pagelen=Settings.MAX_PAGELEN):
        """
        GET with filter support
        """
        def cast(value):
            if self._cast_leaf is None:
                return value
            
            if issubclass(self._cast_leaf, ApiLeaf):
                return self._cast_leaf(self._api_url, data=value)
            else:
                return self._cast_leaf(value)

        return NetworkPagination(
            self._api_url if filter is None else f"{self._api_url}?{filter}",
            cast,
            pagelen=pagelen
        )

    def new(self):
        """
        Create a leaf that will support create function (POST).
        """
        if self._api_unsupported & ApiBranchPagination.NEW > 0:
            raise ApiUnsupported("NEW")
        return self._cast_leaf(self._api_url)
