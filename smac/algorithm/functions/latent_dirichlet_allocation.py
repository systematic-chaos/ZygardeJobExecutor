'''
algorithm/functions/latent_dirichlet_allocation -- Latent Dirichled Allocation (LDA)
Latent Dirichlet Allocation is a topic model which infers topics from a collection
of text documents. LDA can be thought of as a clustering algorithm as follows:
  * Topics corresponde to cluster centers, and documents correspond to examples (rows)
    in a dataset.
  * Topics and documents both exist in a feature space, where feature vectors are vectors
    of word counts (bag of words).
  * Rather than estimating a clustering using traditional distance, LDA uses a function
    based on a statistical model of how text documents are generated.

Zygarde: Platform for reactive training of models in the cloud
Master in Big Data Analytics
Polytechnic University of Valencia

@author:    Javier Fernández-Bravo Peñuela
@copyright: 2020 Ka-tet Corporation. All rights reserved.
@license:   GPLv3.0
@contact:   fjfernandezbravo@iti.es
'''

from pyspark.ml.clustering import LDA
from pyspark.ml.evaluation import ClusteringEvaluator

hyperparameters_default_values = {
    'k': 10,
    'maxIter': 20,
    'optimizer': 'online',
    'featuresCol': 'features',
    'predictionCol': 'prediction'
}

def latent_dirichlet_allocation(spark, data, hyperparameters):
    
    # Trains a LDA model
    lda = LDA(k=hyperparameters['k'], maxIter=hyperparameters['maxIter'],
            featuresCol=hyperparameters['featuresCol'])
    lda_model = lda.fit(data)

    # Make predictions
    predictions = lda_model.transform(data)

    # Evaluate clustering by computing Silhouette score with squared euclidean distance
    evaluator = ClusteringEvaluator(metricName='silhouette', distanceMeasure='squaredEuclidean',
                                    featuresCol=hyperparameters['featuresCol'],
                                    predictionCol=hyperparameters['predictionCol'])
    silhouette = evaluator.evaluate(predictions)

    return silhouette, lda_model

def latent_dirichlet_allocation_func(spark, params={}, data=None):
    hyperparams = hyperparameters_values(params)

    (score, model) = latent_dirichlet_allocation(spark, data, hyperparams)
    return score, model

def hyperparameters_values(params):
    hyperparameters = hyperparameters_default_values.copy()
    for k, v in params.items():
        if k in hyperparameters:
            hyperparameters[k] = v
    return hyperparameters
