'''
linear_support_vector_machine -- Binomial classification: Linear Support Vector Machine

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

from ....aux_functions import hyperparameters_values
from ....evaluation import mcc, confusion_matrix_rates as confusion_matrix

hyperparameters_default_values = {
    'maxIter': 100,
    'regParam': 0.0
}

def linear_support_vector_machine(spark, data, hyperparameters):
    
    # Split the data into train and test
    (training_data, test_data) = data.randomSplit((0.8, 0.2))

    # Create the trainer and set its parameters
    lsvc = LinearSVC(maxIter=hyperparameters['maxIter'], regParam=hyperparameters['regParam'])

    # Train and fit the model
    lsvc_model = lsvc.fit(training_data)

    # Make predictions
    predictions = lsvc_model.transform(test_data)

    # Compute score for binomial classification on the test set
    mcc_score = mcc(*confusion_matrix(predictions))

    return mcc_score, lsvc_model

def linear_support_vector_machine_func(spark, params={}, data=None):
    hyperparams = hyperparameters_values(params, hyperparameters_default_values)

    (score, model) = linear_support_vector_machine(spark, data, hyperparams)
    return score, model
