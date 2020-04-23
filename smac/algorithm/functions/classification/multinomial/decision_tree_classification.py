'''
decision_tree_classification -- Multinomial classification: Decision Tree classifier

Decision trees are a popular family of classification and regression methods.

Zygarde: Platform for reactive training of models in the cloud
Master in Big Data Analytics
Polytechnic University of Valencia

@author:    Javier Fernández-Bravo Peñuela
@copyright: 2020 Ka-tet Corporation. All rights reserved.
@license:   GPLv3.0
@contact:   fjfernandezbravo@iti.es
'''

from pyspark.ml import Pipeline
from pyspark.ml.classification import DecisionTreeClassifier
from pyspark.ml.feature import StringIndexer, VectorIndexer
from pyspark.ml.evaluation import MulticlassClassificationEvaluator

from ....aux_functions import hyperparameters_values

hyperparameters_default_values = {
    'maxDepth': 5,
    'maxCategories': 4
}

def decision_tree_classification(spark, data, hyperparameters):
    
    # Index labels, adding metadata to the label column
    # Fit on whole dataset to include all labels in index
    label_indexer = StringIndexer(inputCol=hyperparameters['labelCol'],
                                    outputCol='indexedLabel').fit(data)
    hyperparameters['labelCol'] = 'indexedLabel'

    # Automatically identify categorical features, and index them
    # We specify maxCategories so features with > 4 distinct values are managed as continuous
    feature_indexer = VectorIndexer(maxCategories=hyperparameters['maxCategories'],
                                    inputCol=hyperparameters['featuresCol'],
                                    outputCol='indexedFeatures').fit(data)
    hyperparameters['featuresCol'] = 'indexedFeatures'

    # Split the data into training and test sets
    (training_data, test_data) = data.randomSplit((0.7, 0.3))

    # Train a Decision Tree Classifier model
    dt = DecisionTreeClassifier(maxDepth=hyperparameters['maxDepth'],
                                featuresCol=hyperparameters['featuresCol'],
                                labelCol=hyperparameters['labelCol'])

    # Chain indexers and tree in a Pipeline
    pipeline = Pipeline(stages=[label_indexer, feature_indexer, dt])

    # Train model; this also runs the indexers
    pipeline_model = pipeline.fit(training_data)

    # Make predictions
    predictions = pipeline_model.transform(test_data)

    # Select and compute test error
    evaluator = MulticlassClassificationEvaluator(metricName='f1',
                                                labelCol=hyperparameters['labelCol'],
                                                predictionCol=hyperparameters['predictionCol'])
    f1_score = evaluator.evaluate(predictions)

    dt_model = pipeline_model.stages[2]
    return f1_score, dt_model

def decision_tree_classification_func(spark, params={}, data=None):
    hyperparams = hyperparameters_values(params, hyperparameters_default_values)

    (score, model) = decision_tree_classification(spark, data, hyperparams)
    return abs(score), model
