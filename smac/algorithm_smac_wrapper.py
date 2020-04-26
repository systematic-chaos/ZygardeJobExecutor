#!/opt/anaconda3/bin/python
# encoding: utf-8

'''
algorithm_smac_wrapper -- Main script for executing Python functions from SMAC

Zygarde: Platform for reactive training of models in the cloud
Master in Big Data Analytics
Polytechnic University of Valencia

@author:    Javier Fernández-Bravo Peñuela
@copyright: 2020 Ka-tet Corporation. All rights reserved.
@license:   GPLv3.0
@contact:   fjfernandezbravo@iti.es
'''

import sys

from algorithm.algorithm_local_wrapper import perform_training

# Compute the target algorithm
try:
    outputValue = perform_training(sys.argv[6:])
    print("Result for SMAC: SUCCESS, 0, 0, %f, 0" % -outputValue, file=sys.stdout)
except ValueError as ve:
    print("Result for SMAC: CRASH, 0, 0, %f, 0" % float(0), file=sys.stdout)
    print("ValueError:", ve, file=sys.stderr)
except Exception as e:
    # Since SMAC tries to minimize the resulting values, an exception causes the maximum value
    # to be returned, avoiding it to become an incumbent candidate
    print("Result for SMAC: CRASH, 0, 0, %f, 0" % float('inf'), file=sys.stdout)
    print(e, file=sys.stderr)
