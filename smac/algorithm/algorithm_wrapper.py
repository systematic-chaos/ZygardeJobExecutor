'''
algorithm_wrapper -- Wrapper for invoking functions from the command-line

@author:    Thánatos Dreamslayer
@copyright: 2020 Ka-tet Corporation. All rights reserved.
@license:   GPLv3.0
@contact:   fraferp9@posgrado.upv.es
'''

from .functions.branin import branin_func as branin

algorithm_modules = { 'branin': branin }

# For black box function optimization, we can ignore the first arguments.
# The remaining arguments specify parameters using this format: -name value
def get_command_line_args(runargs):
    args = {}
    i = runargs.index('-' + 'algorithm') + 2
    algorithm = runargs[i-1]
    while i < len(runargs):
        args[runargs[i][1:]] = cast_argument(runargs[i+1])
        i += 2
    return algorithm, args

def is_int(value):
    try:
        int(value)
        return True
    except ValueError:
        return False

def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

def cast_argument(value):
    if is_int(value):
        return int(value)
    elif is_float(value):
        return float(value)
    else:
        return str(value)
