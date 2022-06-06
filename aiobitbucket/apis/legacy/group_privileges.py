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

from ...typing.legacy.group_privileges import GroupPrivileges, Privilege


class GroupPrivilegesRepoSlug:
    """
    Use the group-privileges resource to query and manipulate the group privileges (permissions) of a Bitbucket Cloudaccount's repositories.

    https://confluence.atlassian.com/bitbucket/group-privileges-endpoint-296093137.html

    Coverage:
    - GET a list of privileged groups for a repository
    - PUT group privileges on a repository
    - DELETE group privileges from a repository
    """

    def __init__(self, network, workspace_name, repo_slug_name):
        self._api_url = f"/1.0/group-privileges/{workspace_name}/{repo_slug_name}"
        self._network = network
        self.default_group_owner = workspace_name

    async def get(self):
        """GET a list of privileged groups for a repository"""
        results = await self._network.get(self._api_url)
        group_privileges = GroupPrivileges({"privileges": results})
        return group_privileges

    async def add(self, group, privilege: Privilege, group_owner=None):
        """PUT group privileges on a repository"""
        await self._network.put(
            "{}/{}/{}".format(
                self._api_url, group_owner or self.default_group_owner, group
            ),
            privilege.value,
        )

    async def delete(self, group, group_owner=None):
        """DELETE group privileges from a repository"""
        await self._network.delete(
            "{}/{}/{}".format(
                self._api_url, group_owner or self.default_group_owner, group
            )
        )
