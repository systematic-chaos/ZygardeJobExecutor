#!/opt/anaconda3/bin/python
# encoding: utf-8

'''
smac_wrapper -- SMAC Python wrapper

Zygarde: Platform for reactive training of models in the cloud
Master in Big Data Analytics
Polytechnic University of Valencia

@author:    Javier Fernández-Bravo Peñuela
@copyright: 2020 Ka-tet Corporation. All rights reserved.
@license:   GPLv3.0
@contact:   fjfernandezbravo@iti.es
'''

from wrapper.generic_smac_wrapper import GenericSmacWrapper

wrapper = GenericSmacWrapper()
wrapper.main()
