# This file is part of LAB CLI.
# Copyright (C) 2025 Rafael Marín Sánchez (rafmarsan - rafa marsan)
# Licensed under the GNU GPLv3. See LICENSE file for details.

# lab/application/use_cases/grader/__init__.py
from .grader_vars import GraderVars
from .grader_role import GraderRole
from .grader_webservers import GraderWebservers
from .grader_databases import GraderDatabases

GRADERS = {
    "vars": GraderVars,
    "role": GraderRole,
    "webservers": GraderWebservers,
    "databases": GraderDatabases,
}
