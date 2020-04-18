'''
algorithm/functions/linear_support_vector_machine - Linear Support Vector Machine
The linear SVM is a standard method for large-scale classification tasks.
It is a linear method, with the loss function in the formulation given by the hinge loss.
A support vector machine constructs a hyperplane or set of hyperplanes on a high- or infinite-
dimensional space, which can be used for classification, regression, or other tasks. Intuitively,
a good separation is achieved by the hyperplane that has the largest distance to the nearest
training-data points of any class (so-called functional margin), since in general the larger
the margin the lower the generalization error of the classifier.

Zygarde: Platform for reactive training of models in the cloud
Master in Big Data Analytics
Polytechnic University of Valencia

@author:    Javier Fernández-Bravo Peñuela
@copyright: 2020 Ka-tet Corporation. All rights reserved.
@license:   GPLv3.0
@contact:   fjfernandezbravo@iti.es
'''

from pyspark.ml.classification import LinearSVC

from ..evaluation import mcc, confusion_matrix_rates as confusion_matrix

hyperparameters_default_values = {
    'maxIter': 100,
    'regParam': 0.0,
    'featuresCol': 'features',
    'labelCol': 'label',
    'predictionCol': 'prediction'
}

def linear_support_vector_machine(spark, data, hyperparameters):
    
    # Split the data into train and test
    (training_data, test_data) = data.randomSplit([0.8, 0.2])

    # Create the trainer and set its parameters
    lsvc = LinearSVC(maxIter=hyperparameters['maxIter'], regParam=hyperparameters['regParam'])

    # Train and fit the model
    lsvc_model = lsvc.fit(training_data)

    # Make predictions
    predictions = lsvc_model.transform(test_data)

    # Compute score for binomial classification on the test set
    score = mcc(*confusion_matrix(predictions))

    return score, lsvc_model

def linear_support_vector_machine_func(spark, params={}, data=None):
    hyperparams = hyperparameters_values(params)

    (score, model) = linear_support_vector_machine(spark, data, hyperparams)
    return score, model

def hyperparameters_values(params):
    hyperparameters = hyperparameters_default_values.copy()
    for k, v in params.items():
        if k in hyperparameters:
            hyperparameters[k] = v
    return hyperparameters
