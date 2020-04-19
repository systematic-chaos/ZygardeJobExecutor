'''
algorithm/functions/multinomial_logistic_regression
Logistic regression is a popular method to predict a categorical response. It is a special case of
Generalized Linear Models that predicts the probability of outcomes.

Zygarde: Platform for reactive training of models in the cloud
Master in Big Data Analytics
Polytechnic University of Valencia

@author:    Javier Fernández-Bravo Peñuela
@copyright: 2020 Ka-tet Corporation. All rights reserved.
@license:   GPLv3.0
@contact:   fjfernandezbravo@iti.es
'''

from pyspark.ml.classification import LogisticRegression
from pyspark.ml.evaluation import MulticlassClassificationEvaluator

from .binomial_logistic_regression import hyperparameters_default_values, hyperparameters_values

def logistic_regression(spark, data, hyperparameters):
    
    # Split the data into training and test sets
    (training_data, test_data) = data.randomSplit([0.75, 0.25])

    # Create the classifier and set its parameters
    lr = LogisticRegression(family='multinomial',
                            maxIter=hyperparameters['maxIter'],
                            regParam=hyperparameters['regParam'],
                            elasticNetParam=hyperparameters['elasticNetParam'])
    
    # Train and fit the model
    lr_model = lr.fit(training_data)

    # Make predictions
    predictions = lr_model.transform(test_data)

    # Compute score for multinomial classification on the test set
    evaluator = MulticlassClassificationEvaluator(metricName='f1')
    score = evaluator.evaluate(predictions)

    return score, lr_model

def logistic_regression_func(spark, params={}, data=None):
    hyperparams = hyperparameters_values(params)

    (f1_score, model) = logistic_regression(spark, data, hyperparams)
    return f1_score, model
