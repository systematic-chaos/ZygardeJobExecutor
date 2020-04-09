'''
branin -- Branin function computation

@author:    Thánatos Dreamslayer
@copyright: 2020 Ka-tet Corporation. All rights reserved.
@license:   GPLv3.0
@contact:   fraferp9@posgrado.upv.es
'''

import math

def branin(x1, x2,
            a = 1,
            b = 5.1 / (4 * math.pi ** 2),
            c = 5 / math.pi,
            r = 6,
            s = 10,
            t = 1 / (8 * math.pi)):
    return a * (x2 - b * x1 * x1 + c * x1 - r) ** 2 + s * (1 - t) * math.cos(x1) + s

def branin_func(args):
    if all(var in args for var in ['x1', 'x2']):
        x1 = args['x1']
        x2 = args['x2']
        if all(var in args for var in ['a', 'b', 'c', 'r', 's', 't']):
            yValue = branin(x1, x2, args['a'], args['b'], args['c'], args['r'], args['s'], args['t'])
        else:
            yValue = branin(x1, x2)
        return -yValue
    else:
        raise ValueError('x1 and x2 input variable arguments were no provided')
