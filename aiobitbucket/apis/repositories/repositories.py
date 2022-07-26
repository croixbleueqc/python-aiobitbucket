"""
https://developer.atlassian.com/bitbucket/api/2/reference/resource/repositories
"""

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

from .repository import RepoSlug


class Repositories(object):
    """
    https://developer.atlassian.com/bitbucket/api/2/reference/resource/repositories
    """

    def __init__(self, network):
        self._network = network

    def repo_slug(self, workspace_name, repo_slug_name):
        """Repository API shortcut accessor"""
        return RepoSlug(self._network, workspace_name, repo_slug_name)
