"""
Typing for Branch Restrictions

https://developer.atlassian.com/bitbucket/api/2/reference/resource/repositories/%7Bworkspace%7D/%7Brepo_slug%7D/branch-restrictions
"""

from typing_engine.typing import Typing2, Field
from enum import Enum

class BranchMatchKind(Enum):
    BRANCHING_MODEL="branching_model"
    GLOB="glob"

    def __str__(self):
        return self.value

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

class Kind(Enum):
    REQUIRE_TASKS_TO_BE_COMPLETED = "require_tasks_to_be_completed"
    FORCE = "force"
    RESTRICT_MERGES = "restrict_merges"
    ENFORCE_MERGE_CHECKS = "enforce_merge_checks"
    REQUIRE_APPROVALS_TO_MERGE = "require_approvals_to_merge"
    DELETE = "delete"
    REQUIRE_ALL_DEPENDENCIES_MERGED = "require_all_dependencies_merged"
    PUSH = "push"
    REQUIRE_PASSING_BUILDS_TO_MERGE = "require_passing_builds_to_merge"
    RESET_PULLREQUEST_APPROVALS_ON_CHANGE = "reset_pullrequest_approvals_on_change"
    REQUIRE_DEFAULT_REVIEWER_APPROVALS_TO_MERGE = "require_default_reviewer_approvals_to_merge"

    def __str__(self):
        return self.value

class BranchType(Enum):
    feature = "feature"
    bugfix = "bugfix"
    release = "release"
    hotfix = "hotfix"
    development = "development"
    production = "production"

    def __str__(self):
        return self.value

class BranchRestriction(Typing2):
    id = Field()
    kind = Field() \
        .converter(loads=Kind, dumps=str)
    branch_match_kind = Field() \
        .converter(loads=BranchMatchKind, dumps=str)
    branch_type = Field() \
        .converter(loads=BranchType, dumps=str)
    pattern = Field()
    groups = Field().list_of()
    users = Field().list_of()
    value = Field()

    def post_dumps(self, raw, dump):
        if self.branch_match_kind != BranchMatchKind.BRANCHING_MODEL:
            # Do not use it when branch_match_kind is not branching_model.
            dump.pop("branch_type")