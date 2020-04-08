#!/opt/anaconda3/bin/python
# encoding: utf-8

import sys

from algorithm.algorithm_wrapper import algorithm_modules, get_command_line_args

# Compute the target algorithm
try:
    algorithm, func_args = get_command_line_args(sys.argv)
    if algorithm in algorithm_modules:
        outputValue = algorithm_modules[algorithm](func_args)

        # SMAC has a few different output fields; here, we only need the 4th output:
        print("Result for SMAC: SUCCESS, 0, 0, %f, 0" % -outputValue)

    else:
        raise ValueError('algorithm function')
except ValueError as ve:
    print(ve)
    print("Result for SMAC: CRASH, 0, 0, %f, 0" % float("inf"))
