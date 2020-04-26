'''
gaussian_mixture_model -- Clustering: Gaussian Mixture Model (GMM)

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
from pyspark.ml.evaluation import ClusteringEvaluator

from ...aux_functions import hyperparameters_values

hyperparameters_default_values = {
    'k': 2,
    'tol': 0.001,
    'maxIter': 100
}

def gaussian_mixture_model(spark, data, hyperparameters):

    # Trains a GMM model
    gmm = GaussianMixture(k=hyperparameters['k'],
                        tol=hyperparameters['tol'],
                        maxIter=hyperparameters['maxIter'],
                        featuresCol=hyperparameters['featuresCol'],
                        predictionCol=hyperparameters['predictionCol'])
    gmm_model = gmm.fit(data)

    # Make predictions
    predictions = gmm_model.transform(data)

    # Evaluate clustering by computing Silhouette score with squared euclidean distance
    evaluator = ClusteringEvaluator(metricName='silhouette', distanceMeasure='squaredEuclidean',
                                    featuresCol=hyperparameters['featuresCol'],
                                    predictionCol=hyperparameters['predictionCol'])
    silhouette_score = evaluator.evaluate(predictions)

    return silhouette_score, gmm_model

def gaussian_mixture_model_func(spark, params={}, data=None):
    hyperparams = hyperparameters_values(params, hyperparameters_default_values)

    (score, model) = gaussian_mixture_model(spark, data, hyperparams)
    return abs(score), model
