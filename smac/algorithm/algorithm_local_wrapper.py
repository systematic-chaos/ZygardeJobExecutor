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
from os import remove as remove_file
from shutil import rmtree as remove_dir
from uuid import uuid4 as uuid

from .s3_object_manager import upload_file
from .aux_functions import merge_dictionaries, cast_argument

from .functions.branin import branin_func as branin
from .functions.linear_regression import linear_regression_func as linear_regression
from .functions.random_forest_regression import random_forest_regression_func as random_forest_regression
from .functions.naive_bayes import naive_bayes_func as naive_bayes
from .functions.linear_support_vector_machine import linear_support_vector_machine_func as lsvm
from .functions.k_means import k_means_func as k_means
from .functions.gaussian_mixture_model import gaussian_mixture_model_func as gmm
from .functions.multilayer_perceptron_classifier import multilayer_perceptron_classifier_func as mlpc
from .functions.latent_dirichlet_allocation import latent_dirichlet_allocation_func as lda
from .functions.random_forest_classification import random_forest_classification_func as random_forest_classification
from .functions.generalized_linear_regression import generalized_linear_regression_func as glrm
from .functions.binomial_logistic_regression import logistic_regression_func as binomial_logistic_regression
from .functions.multinomial_logistic_regression import logistic_regression_func as multinomial_logistic_regression

misc_functions = { 'branin': branin }
regression = { 'linear-regression': linear_regression,
                'generalized-linear-regression': glrm,
                'random-forest-regression': random_forest_regression }
binomial_classification = { 'linear-support-vector-machine': lsvm,
                            'binomial-logistic-regression': binomial_logistic_regression }
multinomial_classification = { 'naive_bayes': naive_bayes,
                    'random-forest-classification': random_forest_classification,
                    'multilayer-perceptron-classifier': mlpc,
                    'multinomial-logistic-regression': multinomial_logistic_regression }
clustering = { 'k-means': k_means,
                'gaussian-mixture-model': gmm,
                'latent-dirichlet-allocation': lda }
classification = merge_dictionaries([multinomial_classification, binomial_classification])

algorithm_modules = merge_dictionaries([misc_functions, regression, classification, clustering])

def perform_training(runargs):
    app_name, algorithm, data_source, func_params = get_command_line_args(runargs)
    if algorithm not in algorithm_modules:
        raise ValueError("algorithm function %s does not exist" % algorithm)

    spark = get_spark_session(app_name)
    data = load_s3_dataset(spark, data_source) if data_source else None
    #spark = None; data = None    # REMOVE ME
    (score, model) = algorithm_modules[algorithm](spark, func_params, data)

    #upload_model_s3(model, app_name, algorithm, score, func_params)

    spark.stop()
    return score

def get_spark_session(app_name):
    spark = SparkSession.builder.master('local').appName(app_name).getOrCreate()
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

def upload_model_s3(model, request_id, algorithm, precision, hyperparams):
    if not model:
        return
    
    model_bucket = 'zygarde-model'

    compose_upload_report(model_bucket, request_id, algorithm, precision, hyperparams)
    save_upload_model(model_bucket, model, request_id, algorithm, precision)

def save_upload_model(s3_bucket, model, request_id, algorithm, precision):
    tmp_model_path = compose_temp_path(request_id, precision, algorithm) + "-model"

    model.write().format('pmml').save(tmp_model_path)
    upload_file(tmp_model_path + "/part-00000", s3_bucket,
        compose_model_path(request_id, precision, algorithm))
    remove_dir(tmp_model_path)

def compose_upload_report(s3_bucket, request_id, algorithm, precision, hyperparams):
    tmp_report_path = compose_temp_path(request_id, precision, algorithm) + "-report"

    with open(tmp_report_path, 'w') as report_file:
        report_file.write(compose_report_message(algorithm, precision, hyperparams))
    upload_file(tmp_report_path, s3_bucket, compose_report_path(request_id, precision, algorithm))
    remove_file(tmp_report_path)

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

def compose_report_message(algorithm, precision, hyperparams):
    report_msg = "%s:\t%1.4f\t" % (algorithm, precision)
    for k, hp in hyperparams.items():
        report_msg += "    %s: %s" % (k, str(hp))
    return report_msg

def compose_path(request_id, precision, algorithm):
    return "%s/%1.4f-%s" % (request_id, precision, algorithm)

def compose_report_path(request_id, precision, algorithm):
    return "%s-%s.%s" % (compose_path(request_id, precision, algorithm), "report", "txt")

def compose_model_path(request_id, precision, algorithm):
    return "%s-%s.%s" % (compose_path(request_id, precision, algorithm), "model", "xml")

def compose_temp_path(request_id, precision, algorithm):
    return "%s/%s-%.4f-%s" % ("/tmp", request_id, precision, algorithm)


