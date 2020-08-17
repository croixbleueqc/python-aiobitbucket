"""
Network Management to request Bitbucket API

network is exposed globaly on this module to simplify implementations
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


import asyncio
import aiohttp

import logging

from .settings import Settings
from .errors import NetworkBadRequest, NetworkForbidden, NetworkNotFound, NetworkUnauthorized, NetworkServerErrors, SessionAlreadyExist

logger = logging.getLogger(Settings.LOG_NETWORK)

class _Network(object):
    """
    Network

    Support standard operations (session, get, post, ...)
    """
    def __init__(self, base_url):
        self.session = None
        self.base_url = base_url

    def basic_auth(self, username, password):
        return aiohttp.BasicAuth(username, password)

    def create_session(self, headers=None, auth=None):
        if self.session is None:
            self.session = aiohttp.ClientSession(headers=headers, auth=auth)
        else:
            raise SessionAlreadyExist()
    
    async def close_session(self):
        if self.session is not None:
            await self.session.close()
        
        await asyncio.sleep(0.250)

    async def answer(self, resp : aiohttp.ClientResponse):
        status = resp.status

        if resp.content_type == "application/json":
            payload = await resp.json()
        else:
            payload = await resp.text()

        logger.debug(f"status={status}, payload={payload}")

        if status in (Settings.SUCCESS, Settings.CREATED, Settings.NO_CONTENT):
            return payload
        elif status == Settings.BAD_REQUEST:
            raise NetworkBadRequest(status, payload)
        elif status == Settings.UNAUTHORIZED:
            raise NetworkUnauthorized(status, payload)
        elif status == Settings.FORBIDDEN:
            raise NetworkForbidden(status, payload)
        elif status == Settings.NOTFOUND:
            raise NetworkNotFound(status, payload)
        else:
            raise NetworkServerErrors(status, payload)

    async def get(self, url : str):
        # Bitbucket pagination returns an absolute url to be used.
        # So we need to handle absolute/relative cases
        final_url = url if url.startswith("http") else self.base_url + url

        async with self.session.get(final_url) as resp:
            return await self.answer(resp)

    async def put(self, url, payload):
        put_keywords = {}
        if isinstance(payload, dict):
            put_keywords["json"]=payload
        else:
            # Support some legacy API calls
            put_keywords["data"]=payload

        async with self.session.put(self.base_url + url, **put_keywords) as resp:
            return await self.answer(resp)
    
    async def post(self, url, payload):
        async with self.session.post(self.base_url + url, json=payload) as resp:
            return await self.answer(resp)

    async def post_form(self, url, payload):
        async with self.session.post(self.base_url + url, data=payload) as resp:
            return await self.answer(resp)

    async def delete(self, url):
        async with self.session.delete(self.base_url + url) as resp:
            await self.answer(resp)

# Unique instance shared by all modules (avoid passing network or core object to all objects)
network = None

class Network(object):
    """
    Network Accessor (wrapper for network instance)
    """
    @classmethod
    def create_unique_instance(cls, base_url):
        global network
        network = _Network(base_url)
        return network

    @classmethod
    def get_unique_instance(cls):
        return network

    @classmethod
    def get(cls, url):
        return network.get(url)

    @classmethod
    def put(cls, url, payload):
        return network.put(url, payload)

    @classmethod
    def post(cls, url, payload):
        return network.post(url, payload)

    @classmethod
    def post_form(cls, url, payload):
        return network.post_form(url, payload)

    @classmethod
    def delete(cls, url):
        return network.delete(url)

class NetworkPagination(object):
    """
    Generic support for pagination

    https://developer.atlassian.com/bitbucket/api/2/reference/meta/pagination
    """

    def __init__(self, url : str, dynamic_cast=None, pagelen=Settings.MAX_PAGELEN):
        if "?" in url:
            self.url = f"{url}&pagelen={pagelen}"
        else:
            self.url = f"{url}?pagelen={pagelen}"
        self.dynamic_cast = dynamic_cast

        logger.debug(f"pagination url: {self.url}")

    def __aiter__(self):
        self._values = []
        self._next = self.url
        return self

    async def __anext__(self):
        value = await self.fetch()

        if value is None:
            raise StopAsyncIteration

        if self.dynamic_cast is None:
            return value
        else:
            return self.dynamic_cast(value)

    async def fetch(self):
        if len(self._values) == 0 and self._next is not None:
            result = await network.get(self._next)
            for value in result["values"]:
                self._values.append(value)
            self._next = result.get("next")

        if len(self._values) > 0:
            return self._values.pop(0)
        else:
            return None
