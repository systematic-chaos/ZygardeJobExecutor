'''
zygardeSmacWrapper -- SMAC wrapper based in genericWrapper.py

@author:    Thánatos Dreamslayer
@copyright: 2020 Ka-tet Corporation. All rights reserved.
@license:   GPLv3.0
@contact:   fraferp9@posgrado.upv.es
'''

import os.path as path

from re import match
from parse import parse

from .genericSmacWrapper import AbstractGenericSmacWrapper

class ZygardeSmacWrapper(AbstractGenericSmacWrapper):

    algorithm_modules = { 'branin': "branin/branin.py" }

    def get_command_line_args(self, runargs, config):
        '''
        Returns the command line call string to execute the target algorithm.
        Args:
            runargs: a map of several optional arguments for the execution of the target algorithm
                {
                    "instance": <instance>,
                    "specifics": <extra data associated with the instance>,
                    "cutoff": <runtime cutoff>,
                    "runlength": <runlength cutoff>,
                    "seed": <seed>
                }
            config: a mapping from parameter name to parameter value
        Returns:
            A command call list to execute the target algorithm.
        '''
        self.algorithm = runargs['specifics']

        root_path = path.normpath(path.join(path.dirname(path.abspath(__file__)), '..'))
        cmd = "python %s " % path.join(root_path, ZygardeSmacWrapper.algorithm_modules[self.algorithm])
        #cmd += " --runsolver-path %s " % path.join(root_path, 'runsolver', 'runsolver')

        # Add the run arguments to cmd
        for key in ['instance', 'specifics', 'cutoff', 'runlength', 'seed']:
            cmd += " %s " % runargs[key]

        # Add the parameters in <config> to cmd
        for name, value in config.items():
            cmd += " -%s %s " % (name[1:], value)
        
        print(cmd)
        return cmd
    
    def process_results(self, filepointer, out_args):
        '''
        Parse a results file to extract the runs status (SUCCESS/CRASHED/etc) and other optional results.

        Args:
            filepointer: a pointer to the file containing the solver execution standard output
            out_args: a map with {"exit_code" : exit code of target algorithm}
        Returns:
            A map containing the standard AClib run results. The current standard result map as of AClib 2.06 is:
            {
                "status": <"SUCCESS"/"SAT"/"UNSAT"/"TIMEOUT"/"CRASHED"/"ABORT">,
                "runtime": <runtime of target algorithm>,
                "quality": <a domain specific measure of the quality of the solution [optional]>,
                "misc": <a (comma-less) string that will be associated with the run [optional]>
            }
            ATTENTION: The return values (i.e., status and runtime) will overwrite
            the measured results of the runsolver (if runsolver was used).
        '''
        # Parse the output of the solver which can be found in the filepointer <filepointer>
        output_data = filepointer.read().decode('utf-8')
        resultMap = { 'misc': self.algorithm }
        
        success_status = ['SUCCESS', 'SATISFIABLE']
        if out_args['exit_code'] == 0 and \
                any([match("Result for SMAC: %s" % status, output_data) for status in success_status]):
            data = parse("Result for SMAC: {}, {}, {}, {}, {}", output_data)
            resultMap['status'] = data[0]
            resultMap['runtime'] = 0
            resultMap['quality'] = -float(data[3])
        else:
            resultMap['status'] = 'CRASHED'
            resultMap['runtime'] = 2147483647
        return resultMap
