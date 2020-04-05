'''
genericSmacWrapper -- template for an AClib target algorithm wrapper

@author:    Thánatos Dreamslayer
@copyright: 2020 Ka-tet Corporation. All rights reserved.
@license:   GPLv3.0
@contact:   fraferp9@posgrado.upv.es
'''

from .genericWrapper import AbstractWrapper

class AbstractGenericSmacWrapper(AbstractWrapper):
    
    def verify_SAT(self, model, solver_output):
        satisfied = True
        with open(self._instance) as fp:
            for line in fp:
                if not(line.startswith('c') or line.startswith('p')):
                    clause = map(int, line.split(' ')[:-1])
                    satisfied &= any(lit in model for lit in clause)
        return satisfied
