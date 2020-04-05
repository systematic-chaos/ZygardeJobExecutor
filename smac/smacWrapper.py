#!/opt/anaconda3/bin/python
# encoding: utf-8

'''
smacWrapper -- SMAC Python wrapper

@author:    Thánatos Dreamslayer
@copyright: 2020 Ka-tet Corporation. All rights reserved.
@license:   GPLv3.0
@contact:   fraferp9@posgrado.upv.es
'''

from smacwrapper.zygardeSmacWrapper import ZygardeSmacWrapper

if __name__ == '__main__':
    wrapper = ZygardeSmacWrapper()
    wrapper.main()
