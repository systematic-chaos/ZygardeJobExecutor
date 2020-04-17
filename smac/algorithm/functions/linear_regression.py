'''
algorithm/functions/linear_regression
Linear regression of polynomial functions, computed via Spark MLlib

Zygarde: Platform for reactive training of models in the cloud
Master in Big Data Analytics
Polytechnic University of Valencia

@author:     Javier Fernández-Bravo Peñuela
@copyright: 2020 Ka-tet Corporation. All rights reserved.
@license:   GPLv3.0
@contact:   fjfernandezbravo@iti.es
'''

from pyspark.ml.regression import LinearRegression
from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession

hyperparameters_default_values = {
    'maxIter': 100,
    'regParam': 0.0,
    'elasticNetParam': 0.0,
    'solver': 'auto',
    'loss': 'squaredError',
    'featuresCol': 'features',
    'labelCol': 'label',
    'predictionCol': 'prediction',
    'weightCol': None
}

def linear_regression(spark, data, hyperparameters):
    lr = LinearRegression(maxIter=hyperparameters['maxIter'],
        regParam=hyperparameters['regParam'],
        elasticNetParam=hyperparameters['elasticNetParam'],
        solver=hyperparameters['solver'],
        loss=hyperparameters['loss'],
        featuresCol=hyperparameters['featuresCol'],
        labelCol=hyperparameters['labelCol'],
        predictionCol=hyperparameters['predictionCol'])

    # Fit the model from training data
    lr_model = lr.fit(data)

    return lr_model.summary.rootMeanSquaredError, lr_model

def linear_regression_func(spark, params={}, data=None):
    hyperparams = hyperparameters_values(params)
    
    (rmse, model) = linear_regression(spark, data, hyperparams)
    return -rmse, model

def hyperparameters_values(params):
    hyperparameters = hyperparameters_default_values.copy()
    for k, v in params.items():
        if k in hyperparameters:
            hyperparameters[k] = v
    return hyperparameters
