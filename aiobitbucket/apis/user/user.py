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

import logging
from ...typing.users.permission import Permission
from ...api import ApiBranchPagination


class Repositories(ApiBranchPagination):
    """
    https://developer.atlassian.com/bitbucket/api/2/reference/resource/user/permissions/repositories

    Coverage:
    - GET: Returns an object for each repository the caller has explicit access to and their effective permission — the highest level of permission the caller has.
           This does not return public repositories that the user was not granted any specific permission in,
           and does not distinguish between direct and indirect privileges.
    """

    def __init__(self, network):
        ApiBranchPagination.__init__(
            self,
            "/2.0/user/permissions/repositories",
            network,
            Permission,
            ApiBranchPagination.NEW,
        )

    async def get_by_full_name(self, repo_full_name):
        """Get permissions for a specific repository"""

        try:
            repos = self.get(f'q=repository.full_name="{repo_full_name}"')
            async for repo in repos:
                return repo
        except Exception as e:
            logging.exception(
                f"Repository '{repo_full_name}'' doesn't exist or you don't have enough privileges to know it ! {e}"
            )


class Permissions(object):
    """
    https://developer.atlassian.com/bitbucket/api/2/reference/resource/user/permissions
    """

    def __init__(self, network):
        # Repositories API accessor
        self.repositories = Repositories(network)


class User(object):
    """
    Covering https://developer.atlassian.com/bitbucket/api/2/reference/resource/user
    """

    def __init__(self, network):
        # Permissions API accessor
        self.permissions = Permissions(network)
