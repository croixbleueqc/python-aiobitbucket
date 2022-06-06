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


class AioBitbucketException(Exception):
    pass


class ApiUnsupported(AioBitbucketException):
    def __init__(self, call_type):
        AioBitbucketException.__init__(self, f"API call {call_type} unsupported")


class NetworkGeneric(AioBitbucketException):
    def __init__(self, msg, status, details):
        super().__init__(msg)
        self.status = status
        self.details = details

    def getNetworkResponse(self):
        return self.status, self.details


class NetworkBadRequest(NetworkGeneric):
    def __init__(self, status, details):
        super().__init__(
            "Something was wrong with the client request.", status, details
        )


class NetworkUnauthorized(NetworkGeneric):
    def __init__(self, status, details):
        super().__init__("Authentication is required", status, details)


class NetworkForbidden(NetworkGeneric):
    def __init__(self, status, details):
        super().__init__(
            "Access to the specified resource is not permitted.", status, details
        )


class NetworkNotFound(NetworkGeneric):
    def __init__(self, status, details):
        super().__init__("The requested resource does not exist.", status, details)


class NetworkServerErrors(NetworkGeneric):
    def __init__(self, status, details):
        super().__init__("Something unexpected went wrong.", status, details)


class SessionAlreadyExist(AioBitbucketException):
    def __init__(self):
        super().__init__("One session already exists !")
