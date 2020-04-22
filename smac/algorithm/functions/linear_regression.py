'''
linear_regression -- Regression: Linear regressor

Linear regression of polynomial functions, computed via Spark MLlib.

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

from ..aux_functions import hyperparameters_values

hyperparameters_default_values = {
    'maxIter': 100,
    'regParam': 0.0,
    'elasticNetParam': 0.0,
    'solver': 'auto',
    'loss': 'squaredError'
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
    
    # Split the data into training and test sets
    (training_data, test_data) = data.randomSplit((0.7, 0.3))

    # Fit the model from training data
    lr_model = lr.fit(training_data)

    # Make predictions
    predictions = lr_model.transform(test_data)

    # Select and compute test error
    evaluator = RegressionEvaluator(metricName='rmse',
                                    labelCol=hyperparameters['labelCol'],
                                    predictionCol=hyperparameters['predictionCol'])
    rmse_score = evaluator.evaluate(predictions)

    return rmse_score, lr_model

def linear_regression_func(spark, params={}, data=None):
    hyperparams = hyperparameters_values(params, hyperparameters_default_values)
    
    (score, model) = linear_regression(spark, data, hyperparams)
    return -score, model
