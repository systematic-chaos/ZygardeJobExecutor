'''
algorithm/functions/k-means
k-means is one of the most commonly used clustering algorithms that clusters the data points
into a predefined number of clusters.
Clustering ins an unsupervised learning problem whereby we aim to group subsets of entities
with one another based on some notion of similarity. Clustering is often used for exploratory
analysis and/or as a component of a hierarchical supervised learning pipeline (in which distinct
classifiers or regression models are trained for each cluster).)

Zygarde: Platform for reactive training of models in the cloud
Master in Big Data Analytics
Polytechnic University of Valencia

@author:    Javier Fernández-Bravo Peñuela
@copyright: 2020 Ka-tet Corporation. All rights reserved.
@license:   GPLV3.0
@contact:   fjfernandezbravo@iti.es
'''

from pyspark.ml.clustering import KMeans
from pyspark.ml.evaluation import ClusteringEvaluator

hyperparameters_default_values = {
        'k': 2,
        'maxIter': 20,
        'initMode': 'k-means||',
        'initSteps': 2,
        'tol': 0.0001,
        'featuresCol': 'features',
        'predictionCol': 'prediction'
}

def k_means(spark, data, hyperparameters):

    # Trains a k-means model
    kmeans = KMeans(k=hyperparameters['k'],
                    maxIter=hyperparameters['maxIter'],
                    initMode=hyperparameters['initMode'],
                    initSteps=hyperparameters['initSteps'],
                    tol=hyperparameters['tol'],
                    featuresCol=hyperparameters['featuresCol'],
                    predictionCol=hyperparameters['predictionCol'])
    km_model = kmeans.fit(data)

    # Make predictions
    predictions = km_model.transform(data)

    # Evaluate clustering by computing Silhouette score with squared euclidean distance
    evaluator = ClusteringEvaluator(metricName='silhouette', distanceMeasure='squaredEuclidean',
                                    featuresCol=hyperparameters['featuresCol'],
                                    predictionCol=hyperparameters['predictionCol'])
    silhouette = evaluator.evaluate(predictions)
    
    return silhouette, km_model

def k_means_func(spark, params={}, data=None):
    hyperparams = hyperparameters_values(params)

    (score, model) = k_means(spark, data, hyperparams)
    return score, model

def hyperparameters_values(params):
    hyperparameters = hyperparameters_default_values.copy()
    for k, v in params.items():
        if k in hyperparameters:
            hyperparameters[k] = v
    return hyperparameters
