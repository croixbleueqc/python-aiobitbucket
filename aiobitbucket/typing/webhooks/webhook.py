"""
Typing for webhook

https://developer.atlassian.com/bitbucket/api/2/reference/resource/workspaces/%7Bworkspace%7D/hooks/%7Buid%7D
"""
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
import typing
from typing_engine.typing import Typing2, Field
from enum import Enum


class event_t(Enum):
    PULL_UNAPPROVED = "pullrequest:unapproved"
    ISSUE_COMMENT_CREATED = "issue:comment_created"
    REPO_IMPORTED = "repo:imported"
    REPO_CREATED = "repo:created"
    REPO_COMMIT_COMMENT_CREATED = "repo:commit_comment_created"
    PULL_APPROVED = "pullrequest:approved"
    PULL_COMMENT_UPDATED = "comment_updated"
    ISSUE_UPDATED = "issue:updated"
    PROJECT_UPDATED = "project:updated"
    REPO_DELETED = "repo:deleted"
    PULL_CHANGES_REQUEST_CREATED = "pullrequest:changes_request_created"
    PULL_COMMENT_CREATED = "pullrequest:comment_created"
    REPO_COMMIT_STATUS_UPDATED = "repo:commit_status_updated"
    PULL_UPDATED = "pullrequest:updated"
    ISSUE_CREATED = "issue:created"
    REPO_FORK = "repo:fork"
    PULL_COMMENT_DELETED = "pullrequest:comment_deleted"
    REPO_COMMIT_STATUS_CREATED = "repo:commit_status_created"
    REPO_UPDATED = "repo:updated"
    PULL_REJECTED = "pullrequest:rejected"
    PULL_FULFILLED = "pullrequest:fulfilled"
    PULL_CREATED = "pullrequest:created"
    PULL_CHANGE_REQUEST_REMOVED = "pullrequest:changes_request_removed"
    REPO_TRANSFER = "repo:transfer"
    REPO_PUSH = "repo:push"

    def __str__(self):
        return self.value


class Event(Typing2):
    value = Field().converter(loads=event_t, dumps=str)


class SubjectType_t(Enum):
    WORKSPACE = "workspace"
    USER = "user"
    REPO = "repository"
    TEAM = "team"

    def __str__(self):
        return self.value


class SubjectType(Typing2):
    value = Field().converter(loads=SubjectType_t, dumps=str)


class WebHookUUID(Typing2):
    uuid = Field()
    description = Field()
    url = Field()
    active = Field().converter(loads=bool)
    events = Field().list_of(inside_instanciator=Event)
    subject_type = SubjectType()
