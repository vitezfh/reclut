from __future__ import unicode_literals

import os
import sys
from contextlib import redirect_stdout
from functools import wraps
from inspect import signature, Parameter

"""Thanks, James @ github.com/jamespreed"""


def verbose(func, default=True):
    @wraps(func)
    def decorator(*args, verbose=default, **kwargs):
        if verbose:
            _stdout = sys.stdout
        else:
            _stdout = open(os.devnull, 'w')
        with redirect_stdout(_stdout):
            return func(*args, **kwargs)

    sig = signature(func)
    param_verbose = Parameter('verbose', Parameter.KEYWORD_ONLY, default=default)
    sig_params = tuple(sig.parameters.values()) + (param_verbose,)
    sig = sig.replace(parameters=sig_params)
    decorator.__signature__ = sig
    return decorator
