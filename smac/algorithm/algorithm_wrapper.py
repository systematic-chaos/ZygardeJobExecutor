from .functions.branin import branin_func as branin

algorithm_modules = { 'branin': branin }

# For black box function optimization, we can ignore the first arguments.
# The remaining arguments specify parameters using this format: -name value
def get_command_line_args(runargs):
    args = {}
    i = runargs.index('-' + 'algorithm') + 2
    algorithm = runargs[i-1]
    while i < len(runargs):
        a = runargs[i+1]
        if is_int(a):
            a = int(a)
        elif is_float(a):
            a = float(a)
        args[runargs[i][1:]] = a
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
