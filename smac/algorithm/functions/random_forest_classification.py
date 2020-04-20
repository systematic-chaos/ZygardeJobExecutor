'''
algorithm/functions/random_forest_classification -- Random forest classification
Random forests are a popular family of classification and regression methods.
Random forests are ensembles of decision trees. They combine many decision trees
for binary and multiclass classification and for regression, using both continuous
and categorical features.

Zygarde: Platform for reactive training of models in the cloud
Master in Big Data Analytics
Polytechnic University of Valencia

@author:    Javier Fernández-Bravo Peñuela
@copyright: 2020 Ka-tet Corporation. All rights reserved.
@license:   GPLv3.0
@contact:   fjfernandezbravo@iti.es
'''

from pyspark.ml import Pipeline
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.feature import IndexToString, StringIndexer, VectorIndexer
from pyspark.ml.evaluation import MulticlassClassificationEvaluator

from .random_forest_regression import hyperparameters_values

hyperparameters_default_values = {
    'numTrees': 20,
    'maxDepth': 5,
    'maxCategories': 4,
    'featuresCol': 'features',
    'labelCol': 'label',
    'predictionCol': 'prediction'
}

def random_forest_classification(spark, data, hyperparameters):
    
    # Index labels, adding metadata to the label column.
    # Fit on whole dataset to include all labels in index.
    label_indexer = StringIndexer(inputCol=hyperparameters['labelCol'],
                                outputCol='indexedLabel').fit(data)
    hyperparameters['labelCol'] = 'indexedLabel'
    
    # Automatically identify categorical features, and index them.
    # Set maxCategories so features with > 4 distinct values are treated as continuous.
    feature_indexer = VectorIndexer(maxCategories=hyperparameters['maxCategories'],
                                    inputCol=hyperparameters['featuresCol'],
                                    outputCol='indexedFeatures').fit(data)
    hyperparameters['featuresCol'] = 'indexedFeatures'

    # Split the data into training and test sets (30 % held out for testing)
    (training_data, test_data) = data.randomSplit([0.7, 0.3])

    # Train a RandomForest model
    rf = RandomForestClassifier(numTrees=hyperparameters['numTrees'],
                                maxDepth=hyperparameters['maxDepth'],
                                labelCol=hyperparameters['labelCol'],
                                featuresCol=hyperparameters['featuresCol'])
    
    # Convert indexed labels back to original labels
    label_converter = IndexToString(inputCol=hyperparameters['predictionCol'],
                                    outputCol='predictedLabel', labels=label_indexer.labels)

    # Chain indexers and random forest classification in a Pipeline
    pipeline = Pipeline(stages=[label_indexer, feature_indexer, rf, label_converter])

    # Train model; this also runs the indexers
    model = pipeline.fit(training_data)

    # Make predictions
    predictions = model.transform(test_data)

    # Select (prediction, true label) and compute test error
    evaluator = MulticlassClassificationEvaluator(metricName='f1',
                    labelCol=hyperparameters['labelCol'],
                    predictionCol=hyperparameters['predictionCol'])
    f1_score = evaluator.evaluate(predictions)

    rf_model = model.stages[2]
    return f1_score, rf_model


def random_forest_classification_func(spark, params={}, data=None):
    hyperparams = hyperparameters_values(params)

    (score, model) = random_forest_classification(spark, data, hyperparams)
    return score, model
