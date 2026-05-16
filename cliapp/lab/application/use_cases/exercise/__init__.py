# This file is part of LAB CLI.
# Copyright (C) 2025 Rafael Marín Sánchez (rafmarsan - rafa marsan)
# Licensed under the GNU GPLv3. See LICENSE file for details.

# lab/application/use_cases/exercise/__init__.py
from .exercise_vars import ExerciseVars
from .exercise_role import ExerciseRole
from .exercise_webservers import ExerciseWebServers
from .exercise_databases import ExerciseDatabases
from .exercise_final import ExerciseFinal

EXERCISES = {
    "vars": ExerciseVars,
    "role": ExerciseRole,
    "webservers": ExerciseWebServers,
    "databases": ExerciseDatabases,
    "final": ExerciseFinal,
}
