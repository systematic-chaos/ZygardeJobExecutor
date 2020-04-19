'''
algorithm/functions/binomial_logistic_regression
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

from ..evaluation import mcc, confusion_matrix_rates as confusion_matrix

hyperparameters_default_values = {
    'maxIter': 100,
    'regParam': 0.0,
    'elasticNetParam': 0.0,
    'featuresCol': 'features',
    'labelCol': 'label',
    'predictionCol': 'prediction'
}

def logistic_regression(spark, data, hyperparameters):
    
    # Split the data into training and test sets
    (training_data, test_data) = data.randomSplit([0.75, 0.25])

    # Create the classifier and set its parameters
    lr = LogisticRegression(family='binomial',
                            maxIter=hyperparameters['maxIter'],
                            regParam=hyperparameters['regParam'],
                            elasticNetParam=hyperparameters['elasticNetParam'])

    # Train and fit the model
    lr_model = lr.fit(training_data)

    # Make predictions
    predictions = lr_model.transform(test_data)

    # Compute score for binomial classification on the test set
    score = mcc(*confusion_matrix(predictions))

    return score, lr_model

def logistic_regression_func(spark, params={}, data=None):
    hyperparams = hyperparameters_values(params)

    (mcc_score, model) = logistic_regression(spark, data, hyperparams)
    return mcc_score, model

def hyperparameters_values(params):
    hyperparameters = hyperparameters_default_values.copy()
    for k, v in params.items():
        if k in hyperparameters:
            hyperparameters[k] = v
    return hyperparameters
