'''
algorithm/functions/naive_bayes -- Multinomial Naive Bayes.
Naive Bayes are a family of simple probabilistic, multiclass classifiers based on applying
Bayes' theorem with strong (naive) independence assumptions between every pair of features.
Naive Bayes can be trained very efficiently. Within a single pass to the training data, it computes the conditional probability distribution
of each feature given label, and then it applies Bayes' theorem to compute the conditional
probability distribution of label given an observation and use it for prediction.

Zygarde: Platform for reactive training of models in the cloud
Master in Big Data Analytics
Polytechnic University of Valencia

@author:    Javier Fernández-Bravo Peñuela
@copyright: 2020 Ka-tet Corporation. All rights reserved.
@license:   GPLv3.0
@contact:   fjfernandezbravo@iti.es
'''

from pyspark.ml.classification import NaiveBayes
from pyspark.ml.evaluation import MulticlassClassificationEvaluator

hyperparameters_default_values = {
    'smoothing': 1.0,
    'modelType': 'multinomial',
    'featuresCol': 'features',
    'labelCol': 'label',
    'predictionCol': 'prediction'
}

def naive_bayes(spark, data, hyperparameters):
    
    # Split the data into train and test
    (training_data, test_data) = data.randomSplit([0.8, 0.2])

    # Create the trainer and set its parameters
    nb = NaiveBayes(modelType=hyperparameters['modelType'],
                    smoothing=hyperparameters['smoothing'])
    
    # Train the model
    nb_model = nb.fit(training_data)

    # Make predictions
    predictions = nb_model.transform(test_data)

    # Compute F1 score on the test set
    evaluator = MulticlassClassificationEvaluator(metricName='f1')
    f1_score = evaluator.evaluate(predictions)

    return f1_score, nb_model


def naive_bayes_func(spark, params={}, data=None):
    hyperparams = hyperparameters_values(params)

    (score, model) = naive_bayes(spark, data, hyperparams)
    return score, model

def hyperparameters_values(params):
    hyperparameters = hyperparameters_default_values.copy()
    for k, v in params.items():
        if k in hyperparameters:
            hyperparameters[k] = v
    return hyperparameters
