'''
gradient_boosted_tree_classification -- Binomial classification: Gradient-Boosted Tree (GBT) classifier

Gradient-boosted trees are a popular classification and regression method using ensembles
of decision trees, which iteratively train in order to minimize a loss function, using both
continuous and categorical features.

Zygarde: Platform for reactive training of models in the cloud
Master in Big Data Analytics
Polytechnic University of Valencia

@author:    Javier Fernández-Bravo Peñuela
@copyright: 2020 Ka-tet Corporation. All rights reserved.
@license:   GPLv3.0
@contact:   fjfernandezbravo@iti.es
'''

from pyspark.ml import Pipeline
from pyspark.ml.classification import GBTClassifier
from pyspark.ml.feature import StringIndexer, VectorIndexer

from ....aux_functions import hyperparameters_values
from ....evaluation import mcc, confusion_matrix_rates as confusion_matrix

hyperparameters_default_values = {
    'maxIter': 20,
    'maxDepth': 5,
    'maxCategories': 4
}

def gradient_boosted_tree_classification(spark, data, hyperparameters):
    
    # Index labels, adding metadata to the label column
    # Fit on the whole dataset to include all labels in index
    label_indexer = StringIndexer(inputCol=hyperparameters['labelCol'],
                                outputCol='indexedLabel').fit(data)
    hyperparameters['labelCol'] = 'indexedLabel'

    # Automatically identify categorical features, and index them
    # Set maxCategories so features with > 4 distinct values are treated as continuous
    feature_indexer = VectorIndexer(maxCategories=hyperparameters['maxCategories'],
                                    inputCol=hyperparameters['featuresCol'],
                                    outputCol='indexedFeatures').fit(data)
    hyperparameters['featuresCol'] = 'indexedFeatures'

    # Split the data into training and test sets
    (training_data, test_data) = data.randomSplit((0.7, 0.3))

    # Train a GBT classifier model
    gbt = GBTClassifier(maxIter=hyperparameters['maxIter'], maxDepth=hyperparameters['maxDepth'],
                        labelCol=hyperparameters['labelCol'],
                        featuresCol=hyperparameters['featuresCol'])
    
    # Chain indexers and GBT in a Pipeline
    pipeline = Pipeline(stages=[label_indexer, feature_indexer, gbt])

    # Train model; this also runs the indexers
    pipeline_model = pipeline.fit(training_data)

    # Make predictions
    predictions = pipeline_model.transform(test_data)

    # Select and compute test error
    mcc_score = mcc(*confusion_matrix(predictions))

    gbt_model = pipeline_model.stages[2]
    return mcc_score, gbt_model

def gradient_boosted_tree_classification_func(spark, params={}, data=None):
    hyperparams = hyperparameters_values(params, hyperparameters_default_values)

    (score, model) = gradient_boosted_tree_classification(spark, data, hyperparams)
    return score, model
