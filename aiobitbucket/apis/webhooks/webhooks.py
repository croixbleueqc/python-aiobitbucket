# Copyright 2022 Croix Bleue du Québec

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
from ...typing.webhooks import webhook


class WebHookUUID(ApiLeaf, webhook.WebHookUUID):
    """
    Manages one webhook

    https://developer.atlassian.com/bitbucket/api/2/reference/resource/workspaces/%7Bworkspace%7D/hooks/%7Buid%7D

    Coverage:
    - DELETE : Deletes the specified webhook subscription from the given workspace.
    - GET : Returns the webhook with the specified id installed on the given workspace.
    - PUT : Updates the specified webhook subscription.
            The following properties can be mutated:
                description
                url
                active
                events
    """

    def __init__(self, api_url_workspace, network, uid=None, data=None, parent=None):
        ApiLeaf(
            api_url_workspace + f"/hooks/{uid}", network, api_unsupported=ApiLeaf.CREATE
        )
        self._network = network
        self.id = uid
        self.data = data


class WebHooks(ApiBranchPagination):
    """
    Manages WebHooks

    https://developer.atlassian.com/bitbucket/api/2/reference/resource/workspaces/%7Bworkspace%7D/hooks
    """

    def __init__(self, network):
        self.network = network

    async def get_by_workspace(self, api_url_workspace):
        ApiBranchPagination.__init__(
            self, api_url_workspace + "/hooks", self.network, WebHookUUID
        )

    async def get_by_repository_name(self, workspace, repo_name):
        """Get hooks for a specific repository"""

        subscription_endpoint = f"/2.0/repositories/{workspace}/{repo_name}/hooks"

        subscriptions = await self.network.get(subscription_endpoint)

        return subscriptions

    async def create_subscription(
        self,
        workspace,
        repo_name,
        url,
        active,
        events,
        description,
    ):
        subscription_endpoint = f"/2.0/repositories/{workspace}/{repo_name}/hooks"
        payload = {
            "description": description,
            "url": url,
            "active": active,
            "events": events,
        }
        subscription = await self.network.post(subscription_endpoint, payload)

        return subscription
