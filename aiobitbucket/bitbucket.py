# Copyright 2020-2022 Croix Bleue du Québec

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

from .network import Network
from .apis.user.user import User
from .apis.repositories.repositories import Repositories
from .apis.webhooks.webhooks import WebHooks


class Bitbucket(object):
    """Bitbucket API main entrypoints"""

    def __init__(self, base_url="https://api.bitbucket.org"):
        self.network = Network(base_url)
        self.user = User(self.network)
        self.repositories = Repositories(self.network)
        self.webhooks = WebHooks(self.network)

    def open_basic_session(self, username, password):
        """Connect to the API with basic authentication"""

        self.network.create_session(auth=self.network.basic_auth(username, password))

    async def close_session(self):
        """Clean up the session"""
        await self.network.close_session()
