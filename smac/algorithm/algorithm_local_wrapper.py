'''
algorithm/algorithm_local_wrapper
Wrapper for invoking functions from the command-line
Useful for local development and debugging

Zygarde: Platform for reactive training of models in the cloud
Master in Big Data Analytics
Polytechnic University of Valencia

@author:    Javier Fernández-Bravo Peñuela
@copyright: 2020 Ka-tet Corporation. All rights reserved.
@license:   GPLv3.0
@contact:   fjfernandezbravo@iti.es
'''

import numpy as np

from pyspark.sql import SparkSession
from os import getenv
from random import randint
from shutil import rmtree as remove_dir
from uuid import uuid4 as uuid

from .aux_functions import merge_dictionaries, cast_argument

from .functions import branin
from .functions import linear_regression
from .functions import random_forest_regression
from .functions import random_forest_regression
from .functions import naive_bayes
from .functions import linear_support_vector_machine as lsvm
from .functions import k_means
from .functions import gaussian_mixture_model as gmm
from .functions import multilayer_perceptron_classifier as mlpc
from .functions import random_forest_classification
from .functions import generalized_linear_regression as glrm
from .functions import binomial_logistic_regression
from .functions import multinomial_logistic_regression
from .functions import decision_tree_classification
from .functions import decision_tree_regression
from .functions import gradient_boosted_tree_classification as gbt_classification
from .functions import gradient_boosted_tree_regression as gbt_regression

misc_functions = { 'branin': branin }
regression = { 'linear-regression': linear_regression,
                'generalized-linear-regression': glrm,
                'random-forest-regression': random_forest_regression,
                'decision-tree-regression': decision_tree_regression,
                'gradient-boosted-tree-regression': gbt_regression }
binomial_classification = { 'linear-support-vector-machine': lsvm,
                            'binomial-logistic-regression': binomial_logistic_regression }
multinomial_classification = { 'naive-bayes': naive_bayes,
                    'random-forest-classification': random_forest_classification,
                    'multinomial-logistic-regression': multinomial_logistic_regression,
                    'decision-tree-classification': decision_tree_classification,
                    'gradient-boosted-tree-classification': gbt_classification }
clustering = { 'k-means': k_means,
                'gaussian-mixture-model': gmm }
deep_learning = { 'multilayer-perceptron-classifier': mlpc }
classification = merge_dictionaries([multinomial_classification, binomial_classification])

algorithm_modules = merge_dictionaries([regression, classification, clustering, deep_learning, misc_functions])
algorithm_platform = { 'standalone': [*misc_functions],
                        'spark': [*merge_dictionaries([regression, classification, clustering, deep_learning])],
                        'horovod': []} 

def perform_training(runargs):
    app_name, algorithm, data_source, func_params = get_command_line_args(runargs)
    if algorithm not in algorithm_modules:
        raise ValueError("algorithm function %s does not exist" % algorithm)

    if algorithm in algorithm_platform['standalone']:
        return perform_standalone_training(algorithm, func_params, data_source)
    elif algorithm in algorithm_platform['spark']:
        return perform_spark_training(algorithm, func_params, data_source, app_name)
    elif algorithm in algorithm_platform['horovod']:
        return float(0)

def perform_standalone_training(algorithm, func_params, data_source=None):
    score = algorithm_modules[algorithm](func_params, data_source)
    return score

def perform_spark_training(algorithm, func_params, data_source, app_name):
    spark = get_spark_session(app_name)

    try:
        data = load_s3_dataset(spark, data_source) if data_source else None
        (score, model) = algorithm_modules[algorithm](spark, func_params, data)
    finally:
        spark.stop()

    return score

def get_spark_session(app_name):
    spark_master = getenv('SPARK_MASTER_HOST', 'localhost')
    spark_session_id = "%s_%d" % (app_name, randint(0, 1048575))
    spark = SparkSession.builder.master('spark://%s:7077' % spark_master)\
                                .appName(spark_session_id).getOrCreate()
    spark.sparkContext.setLogLevel('WARN')
    return spark

# Load and parse the data file, converting it to a DataFrame
def load_s3_dataset(spark, data_source, num_features=None):
    if 'format' in data_source:
        df_reader = spark.read.format(data_source['format'])
        if num_features:
            dataset = df_reader.load(data_source['path'], numFeatures=num_features)
        else:
            dataset = df_reader.load(data_source['path'])
    else:
        dataset = spark.textFile(data_source['path']).map(lambda line: np.array([float(x) for x in line.split(' ')]))
    return dataset

# For black box function optimization, we can ignore the first arguments.
# The remaining arguments specify parameters using this format: -name value,
# except algorithm and data, which are preceded by two dashes.
def get_command_line_args(runargs):
    request_id = str(uuid())
    algorithm = None
    dataset = {}
    args = {}

    i = 0
    while i < len(runargs):
        a = runargs[i][1:]
        if a == '-' + 'id':
            request_id = runargs[i+1]
        elif a == '-' + 'algorithm':
            algorithm = runargs[i+1]
        elif a == '-' + 'dataset':
            dataset['path'] = runargs[i+1]
        elif a == '-dataFormat':
            dataset['format'] = runargs[i+1]
        else:
            args[a] = cast_argument(runargs[i+1])
        i += 2
    return request_id, algorithm, dataset, args
