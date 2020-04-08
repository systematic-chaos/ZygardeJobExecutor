#!/opt/anaconda3/bin/python
# encoding: utf-8

import sys

from algorithm.algorithm_wrapper import algorithm_modules, get_command_line_args

# Compute the target algorithm
try:
    algorithm, func_args = get_command_line_args(sys.argv)
    if algorithm in algorithm_modules:
        outputValue = algorithm_modules[algorithm](func_args)
        print("%f" % outputValue)
    else:
        raise ValueError('algorithm function')
except:
    print("%f" % float("-inf"))
