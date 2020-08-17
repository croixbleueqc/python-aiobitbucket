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
from ...network import Network

class Src(object):
    """
    Manages source code files

    https://developer.atlassian.com/bitbucket/api/2/reference/resource/repositories/{workspace}/{repo_slug}
    https://developer.atlassian.com/bitbucket/api/2/reference/resource/repositories/%7Bworkspace%7D/%7Brepo_slug%7D/src/%7Bnode%7D/%7Bpath%7D
    """
    def __init__(self, api_url_reposlug):
        self._api_url = api_url_reposlug + "/src"

    async def download(self, node, path):
        return await Network.get(f"{self._api_url}/{node}/{path}")
    
    async def upload_pure_text(self, filename, txt, message, author, branch):
        data = {
            filename: txt,
            "message": message,
            "author": author,
            "branch": branch
        }

        return await Network.post_form(self._api_url, data)
