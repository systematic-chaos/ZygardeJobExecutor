'''
algorithm/algorithm_wrapper
Wrapper for invoking functions from the command-line

Zygarde: Platform for reactive training of models in the cloud
Master in Big Data Analytics
Polytechnic University of Valencia

@author:    Javier Fernández-Bravo Peñuela
@copyright: 2020 Ka-tet Corporation. All rights reserved.
@license:   GPLv3.0
@contact:   fjfernandezbravo@iti.es
'''

from pyspark.sql import SparkSession

from .functions.branin import branin_func as branin
from .functions.linear_regression import linear_regression_func as linear_regression

algorithm_modules = { 'branin': branin,
                    'linear-regression': linear_regression }

def perform_training(app_name, runargs):
    algorithm, data_source, func_params = get_command_line_args(runargs)
    if algorithm not in algorithm_modules:
        raise ValueError("algorithm function %s does not exist" % algorithm)

    spark = get_spark_session(app_name)
    data = load_s3_dataset(spark, data_source) if data_source else None
    #spark = None; data = None    # REMOVE ME
    score = algorithm_modules[algorithm](spark, func_params, data)
    spark.stop()
    return score

def get_spark_session(app_name):
    spark = SparkSession.builder.master('local').appName(app_name).getOrCreate()
    spark.sparkContext.setLogLevel('ERROR')
    return spark

def load_s3_dataset(spark, data_source, num_features=None):
    df_reader = spark.read
    if 'format' in data_source:
        df_reader = df_reader.format(data_source['format'])
    if num_features:
        dataset = df_reader.load(data_source['path'], numFeatures=num_features)
    else:
        dataset = df_reader.load(data_source['path'])
    return dataset

# For black box function optimization, we can ignore the first arguments.
# The remaining arguments specify parameters using this format: -name value,
# except algorithm and data, which are preceded by two dashes.
def get_command_line_args(runargs):
    algorithm = None
    dataset = {}
    args = {}

    i = 0
    while i < len(runargs):
        a = runargs[i][1:]
        if a == '-' + 'algorithm':
            algorithm = runargs[i+1]
        elif a == '-' + 'dataset':
            dataset['path'] = runargs[i+1]
        elif a == '-dataFormat':
            dataset['format'] = runargs[i+1]
        else:
            args[a] = cast_argument(runargs[i+1])
        i += 2
    return algorithm, dataset, args

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

def cast_argument(value):
    if is_int(value):
        return int(value)
    elif is_float(value):
        return float(value)
    else:
        return str(value)
