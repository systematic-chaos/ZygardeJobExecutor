#!/opt/anaconda3/bin/python
# encoding: utf-8

'''
algorithm_zygarde_wrapper -- Main script for executing Python functions from a Java process,
                            according to the output syntax expected by Zygarde

@author:    Javier Fernández-Bravo Peñuela
Platform for reactive training of models in the cloud
Master in Big Data Analytics
Polytechnic University of Valencia
@copyright: 2020 Ka-tet Corporation. All rights reserved.
@license:   GPLv3.0
@contact:   fjfernandezbravo@iti.es
'''

import sys

from algorithm.algorithm_wrapper import perform_training

# Compute the target algorithm
try:
    outputValue = perform_training("algorithm_asfd", sys.argv[1:])
    print("Result for Zygarde: %s\t%f" % ('SUCCESS', outputValue), file=sys.stdout)
except ValueError as ve:
    print("Result for Zygarde: %s\t%f" % ('CRASH', float(0)), file=sys.stdout)
    print("ValueError:", ve, file=sys.stderr)
except Exception as e:
    # An exception causes minus infinite to be returned,
    # discarding it from becoming a precision value to be
    # considered as an incumbent candidate
    print("Result for Zygarde: %s\t%f" % ('CRASH', float('-inf')), file=sys.stdout)
    print(e, file=sys.stderr)
