'''
generalized_linear_regression -- Regression: Generalized Linear Model (GLM)

Contrasted with linear regression where the output is assumed to follow a Gaussian distribution,
generalized linear models are specifications of linear models where the response variable
follows some distribution from the exponential family of distributions.

Zygarde: Platform for reactive training of models in the cloud
Master in Big Data Analytics
Polytechnic University of Valencia

@author:    Javier Fernández-Bravo Peñuela
@copyright: 2020 Ka-tet Corporation. All rights reserved.
@license:   GPLv3.0
@contact:   fjfernandezbravo@iti.es
'''

from pyspark.ml.regression import GeneralizedLinearRegression
from pyspark.ml.evaluation import RegressionEvaluator

from ...aux_functions import hyperparameters_values

hyperparameters_default_values = {
    'maxIter': 25,
    'regParam': 0.0,
    'family': 'gaussian',
    'link': 'identity'
}

def generalized_linear_regression(spark, data, hyperparameters):
    glr = GeneralizedLinearRegression(family=hyperparameters['family'],
                                    link=hyperparameters['link'],
                                    maxIter=hyperparameters['maxIter'],
                                    regParam=hyperparameters['regParam'])
    
    # Split the data into training and test sets
    (training_data, test_data) = data.randomSplit((0.7, 0.3))

    # Fit the model from training data
    glr_model = glr.fit(training_data)

    # Make predictions
    predictions = glr_model.transform(test_data)

    # Select and compute test error
    evaluator = RegressionEvaluator(metricName='rmse',
                                    labelCol=hyperparameters['labelCol'],
                                    predictionCol=hyperparameters['predictionCol'])
    rmse_score = evaluator.evaluate(predictions)

    return rmse_score, glr_model

def generalized_linear_regression_func(spark, params={}, data=None):
    hyperparams = hyperparameters_values(params, hyperparameters_default_values)

    (score, model) = generalized_linear_regression(spark, data, hyperparams)
    return -abs(score), model
