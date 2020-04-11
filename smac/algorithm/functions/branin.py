'''
algorithm/functions/branin
Branin function computation

Zygarde: Platform for reactive training of models in the cloud
Master in Big Data Analytics
Polytechnic of University of Valencia

@author:    Javier Fernández-Bravo Peñuela
@copyright: 2020 Ka-tet Corporation. All rights reserved.
@license:   GPLv3.0
@contact:   fjfernandezbravo@iti.es
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

def branin_func(spark, params={}, data=None):
    if all(var in params for var in ['x1', 'x2']):
        x1 = params['x1']
        x2 = params['x2']
        if all(var in params for var in ['a', 'b', 'c', 'r', 's', 't']):
            yValue = branin(x1, x2, params['a'], params['b'], params['c'], params['r'], params['s'], params['t'])
        else:
            yValue = branin(x1, x2)
        return -yValue
    else:
        raise ValueError('x1 and x2 input variable arguments were no provided')
