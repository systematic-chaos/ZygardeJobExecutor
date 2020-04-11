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
    'elasticNetParam': 0.0
}

def linear_regression(spark, data, hyperparameters):
    lr = LinearRegression(maxIter=hyperparameters['maxIter'],
        regParam=hyperparameters['regParam'],
        elasticNetParam=hyperparameters['elasticNetParam'])
    return lr.fit(data)

def linear_regression_func(spark, params={}, data=None):
    hyperparameters = hyperparameters_default_values.copy()
    for k, v in params.items():
        if k in hyperparameters:
            hyperparameters[k] = v
    
    lr_model = linear_regression(spark, data, hyperparameters)
    print("MSE:  %.4f" % lr_model.summary.meanSquaredError)
    print("RMSE: %.4f" % lr_model.summary.rootMeanSquaredError)
    return -lr_model.summary.rootMeanSquaredError
