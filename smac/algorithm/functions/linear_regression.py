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
from pyspark.ml.evaluation import RegressionEvaluator

hyperparameters_default_values = {
    'maxIter': 100,
    'regParam': 0.0,
    'elasticNetParam': 0.0,
    'solver': 'auto',
    'loss': 'squaredError',
    'featuresCol': 'features',
    'labelCol': 'label',
    'predictionCol': 'prediction'
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
    
    # Split the data into training and test sets (30% held for testing)
    (training_data, test_data) = data.randomSplit([0.7, 0.3])

    # Fit the model from training data
    lr_model = lr.fit(training_data)

    # Make predictions
    predictions = lr_model.transform(test_data)

    # Select and compute test error
    evaluator = RegressionEvaluator(metricName='rmse',
                                    labelCol=hyperparameters['labelCol'],
                                    predictionCol=hyperparameters['predictionCol'])
    rmse = evaluator.evaluate(predictions)

    return rmse, lr_model

def linear_regression_func(spark, params={}, data=None):
    hyperparams = hyperparameters_values(params)
    
    (rmse_score, model) = linear_regression(spark, data, hyperparams)
    return -rmse_score, model

def hyperparameters_values(params):
    hyperparameters = hyperparameters_default_values.copy()
    for k, v in params.items():
        if k in hyperparameters:
            hyperparameters[k] = v
    return hyperparameters
