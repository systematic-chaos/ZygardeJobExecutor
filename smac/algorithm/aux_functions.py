'''
algorithm/aux_functions

Zygarde: Platform for reactive training of models in the cloud
Master in Big Data Analytics
Polytechnic University of Valencia

@author:    Javier Fernández-Bravo Peñuela
@copyright: 2020 Ka-tet Corporation. All rights reserved.
@license:   GPLv3.0
@contact:   fjfernandezbravo@iti.es
'''

def merge_dictionaries(d):
    if len(d) > 2:
        return {**merge_dictionaries(d[1:]), **d[0]}
    elif len(d) == 2:
        return {**d[1], **d[0]}
    else:
        return d

def cast_argument(value):
    if is_int(value):
        return int(value)
    elif is_float(value):
        return float(value)
    else:
        return str(value)

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
