"""Sample file with intentional issues for validating linting tools.

Run each tool against this file to verify it detects problems:

    ruff check samples/lint_sample.py
    mypy samples/lint_sample.py
    pylint samples/lint_sample.py
    yapf --diff samples/lint_sample.py
"""

import os                                       # ruff F401 / pylint W0611: unused import
import json                                     # ruff F401 / pylint W0611: unused import
from typing import List, Dict                   # ruff UP006: use builtin list/dict instead


def untyped_function(x, y):                     # mypy / ruff ANN: missing type annotations
    result =  x+y                               # yapf: bad spacing
    if result>0:                                 # yapf: missing spaces around operator
        return result
                                                # mypy: missing return on else branch


def bad_return_type(name: str) -> int:
    return name                                 # mypy: incompatible return type (str vs int)


class bad_class_name:                           # ruff N801: class should use CapWords
    x = 1
    def get_x(self):                            # ruff ANN / pylint C0116: missing docstring
        unused_var = 42                         # ruff F841: local variable never used
        return self.x


def too_many_params(a,b,c,d,e,f,g,h,i,j):      # pylint R0913: too many arguments; yapf: spacing
    return a


def uses_old_typing(items: List[str]) -> Dict[str, int]:  # ruff UP006: use list/dict
    return {item: len(item) for item in items}


x=1                                             # yapf: missing spaces around =
y =  2                                          # yapf: extra space

this_is_a_variable_name_that_is_extremely_long_and_will_absolutely_exceed_our_column_limit = "over 99 chars"  # yapf: line too long
