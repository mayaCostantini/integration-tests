#!/usr/bin/env python3
# Thoth's integration tests
# Copyright(C) 2019 Red Hat, Inc.
#
# This program is free software: you can redistribute it and / or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""Integration tests for Thoth deployment for solvers available."""

import os
import requests

from behave import given, when, then
from hamcrest import assert_that, contains_inanyorder


@given(u'a set of solvers')
def step_impl(context):
    """Take list of solvers from table."""
    context.result = {}
    requested_solvers = []
    for row in context.table:
        requested_solvers.append(row["solver_name"])
    context.result["requested_solvers"] = requested_solvers


@when(u'we ask if the solvers are available')
def step_impl(context):
    """Retrieve available solvers."""
    url = f"{context.scheme}://{context.management_api_url}/api/v1/solvers"
    data = requests.get(url).json()
    available_solvers = [str(solver["solver_name"]) for solver in data["solvers"]["python"]]
    context.result["available_solvers"] = available_solvers


@then(u'we should find the solvers available')
def step_impl(context):
    """Verify all requested solvers are available."""
    print(context.result)
    assert_that(context.result["available_solvers"], contains_inanyorder(context.result["requested_solvers"]))
