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
    def __init__(self, api_url, name=None, data=None, parent=None):
        ApiLeaf.__init__(self, api_url, api_unsupported=ApiLeaf.CREATE | ApiLeaf.UPDATE)
        refs.Branch.__init__(self, data=data, parent=parent)

        if name is not None:
            self.name = name
    
    def _generate_api_url(self):
        if self.name is None:
            return self._api_url
        else:
            return "{}/{}".format(
                self._api_url,
                self.name
            )

class Branches(ApiBranchPagination):
    def __init__(self, api_url_refs):
        ApiBranchPagination.__init__(self, api_url_refs + "/branches", Branch)

class Refs(object):
    def __init__(self, api_url_reposlug):
        self.branches = Branches(api_url_reposlug + "/refs")
