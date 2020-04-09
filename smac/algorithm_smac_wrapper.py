#!/opt/anaconda3/bin/python
# encoding: utf-8

'''
algorithm_smac_wrapper -- Main script for executing Python functions from SMAC

@author:    Thánatos Dreamslayer
@copyright: 2020 Ka-tet Corporation. All rights reserved.
@license:   GPLv3.0
@contact:   fraferp9@posgrado.upv.es
'''

import sys

from algorithm.algorithm_wrapper import algorithm_modules, get_command_line_args

# Compute the target algorithm
try:
    algorithm, func_args = get_command_line_args(sys.argv)
    if algorithm in algorithm_modules:
        outputValue = algorithm_modules[algorithm](func_args)

        # SMAC has a few different output fields; here, we only need the 4th output.
        # Since SMAC tries to minimize the output value (taking it as loss while it
        # actually is the accuracy measure), we negate it, so that it will be maximized
        # according to its absolute value.
        print("Result for SMAC: SUCCESS, 0, 0, %f, 0" % -outputValue, file=sys.stdout)

    else:
        raise ValueError("algorithm function %s does not exist" % algorithm)

except ValueError as ve:
    print("Result for SMAC: CRASH, 0, 0, %f, 0" % float(0), file=sys.stdout)
    print("ValueError:", ve, file=sys.stderr)
except Exception as e:
    # Since SMAC tries to minimize the resulting values, an exception causes the maximum value
    # to be returned, avoiding it to become an incumbent candidate
    print("Result for SMAC: CRASH, 0, 0, %f, 0" % float('inf'), file=sys.stdout)
    print(e, file=sys.stderr)
