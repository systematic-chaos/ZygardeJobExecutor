#!/opt/anaconda3/bin/python
# encoding: utf-8

import sys, math

def branin(x1, x2,
            a = 1,
            b = 5.1 / (4 * math.pi ** 2),
            c = 5 / math.pi,
            r = 6,
            s = 10,
            t = 1 / (8 * math.pi)):
    return a * (x2 - b * x1 * x1 + c * x1 - r) ** 2 + s * (1 - t) * math.cos(x1) + s

# For black box function optimization, we can ignore the first five arguments.
# The remaining arguments specify parameters using this format: -name value
def get_command_line_args(runargs):
    x1 = 0
    x2 = 0
    for i in range(len(runargs) - 1):
        if runargs[i] == '-x1':
            x1 = float(runargs[i+1])
        elif sys.argv[i] == '-x2':
            x2 = float(runargs[i+1])
    return x1, x2




# Compute the branin function
x1, x2 = get_command_line_args(sys.argv)
yValue = branin(x1, x2)

# SMAC has a few different output fields; here, we only need the 4th output:
print("Result for SMAC: SUCCESS, 0, 0, %f, 0" % yValue)
