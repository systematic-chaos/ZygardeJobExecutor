'''
algorithm/functions/gaussian_mixture_model -- Gaussian Mixture Model (GMM)
A Gaussian Mixture Model represents a composite distribution whereby points are drawn fron one of k
Gaussian sub-distributions, each with its own probability. This implementation uses the expectation-
maximization algorithm to induce the maximum-likelihood model given a set of samples.

Zygarde: Platform for reactive training of models in the cloud
Master in Big Data Analytics
Polytechnic University of Valencia

@author:    Javier Fernández-Bravo Peñuela
@copyright: 2020 Ka-tet Corporation. All rights reserved.
@license:   GPLv3.0
@contact:   fjfernandezbravo@iti.es
'''

from pyspark.ml.clustering import GaussianMixture

hyperparameters_default_values = {
    'k': 2,
    'tol': 0.001,
    'maxIter': 100,
    'featuresCol': 'features',
    'predictionCol': 'prediction',
    'probabilityCol': 'probability'
}

def gaussian_mixture_model(spark, data, hyperparameters):
    gmm = GaussianMixture(k=hyperparameters_default_values['k'],
                        tol=hyperparameters_default_values['tol'],
                        maxIter=hyperparameters_default_values['maxIter'],
                        featuresCol=hyperparameters_default_values['featuresCol'],
                        predictionCol=hyperparameters_default_values['predictionCol'])

    model = gmm.fit(data)

    return model.summary.logLikelihood, model

def gaussian_mixture_model_func(spark, params={}, data=None):
    hyperparams = hyperparameters_values(params)

    (score, model) = gaussian_mixture_model(spark, data, hyperparams)
    return abs(score), model

def hyperparameters_values(params):
    hyperparameters = hyperparameters_default_values.copy()
    for k, v in params.items():
        if k in hyperparameters:
            hyperparameters[k] = v
    return hyperparameters
