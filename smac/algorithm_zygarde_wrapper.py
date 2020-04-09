#!/opt/anaconda3/bin/python
# encoding: utf-8

'''
algorithm_zygarde_wrapper -- Main script for executing Python functions from a Java process,
                            according to the output syntax expected by Zygarde

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

        print("Result for Zygarde: %s\t%f" % ('SUCCESS', outputValue), file=sys.stdout)
    
    else:
        raise ValueError("algorithm function %s does not exist" % algorithm)

except ValueError as ve:
    print("Result for Zygarde: %s\t%f" % ('CRASH', float(0)), file=sys.stdout)
    print("ValueError:", ve, file=sys.stderr)
except Exception as e:
    # An exception causes minus infinite to be returned,
    # discarding it from becoming a precision value to be
    # considered as an incumbent candidate
    print("Result for Zygarde: %s\t%f" % ('CRASH', float('-inf')), file=sys.stdout)
    print(e, file=sys.stderr)
