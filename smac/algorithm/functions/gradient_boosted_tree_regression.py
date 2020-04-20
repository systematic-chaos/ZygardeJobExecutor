'''
algorithm/functions/gradient_boosted_tree_regression - Gradient-boosted tree (GBT) regressor
Gradient-boosted trees are a popular classification and regression method using ensembles
of decision trees, which iteratively train in order to minimize a loss function, using both
continuous and categorical features.

Zygarde: Platform for reactive training in the cloud
Master in Big Data Analytics
Polytechnic University of Valencia

@author:    Javier Fernández-Bravo Peñuela
@copyright: 2020 Ka-tet Corporation. All rights reserved.
@license:   GPLv3.0
@contact:   fjfernandezbravo@iti.es
'''

from pyspark.ml import Pipeline
from pyspark.ml.regression import GBTRegressor
from pyspark.ml.feature import VectorIndexer
from pyspark.ml.evaluation import RegressionEvaluator

hyperparameters_default_values = {
    'maxIter': 20,
    'maxDepth': 5,
    'maxCategories': 4,
    'labelCol': 'label',
    'featuresCol': 'features',
    'predictionCol': 'prediction'
}

def gradient_boosted_tree_regression(spark, data, hyperparameters):
    
    # Automatically identify categorical features, and index them
    # Set maxCategories so features with > 4 distinct values are treated as continuous
    feature_indexer = VectorIndexer(maxCategories=hyperparameters['maxCategories'],
                                    inputCol=hyperparameters['featuresCol'],
                                    outputCol='indexedFeatures').fit(data)
    hyperparameters['featuresCol'] = 'indexedFeatures'

    # Split the data into training and test sets (30% held out for testing)
    (training_data, test_data) = data.randomSplit([0.7, 0.3])

    # Train a Gradient Boosed Tree regression model
    gbt = GBTRegressor(maxIter=hyperparameters['maxIter'],
                        maxDepth=hyperparameters['maxDepth'],
                        featuresCol=hyperparameters['featuresCol'])
    
    # Chain indexer and GBT in a pipeline
    pipeline = Pipeline(stages=[feature_indexer, gbt])

    # Training model; this also runs the indexer
    model = pipeline.fit(training_data)

    # Make predictions
    predictions = model.transform(test_data)

    # Select and compute test error
    evaluator = RegressionEvaluator(metricName='rmse',
        labelCol=hyperparameters['labelCol'],
        predictionCol=hyperparameters['predictionCol'])
    rmse_score = evaluator.evaluate(predictions)

    gbt_model = model.stages[1]
    return rmse_score, gbt_model

def gradient_boosted_tree_regression_func(spark, params={}, data=None):
    hyperparams = hyperparameters_values(params)

    (score, model) = gradient_boosted_tree_regression(spark, data, hyperparams)
    return -score, model

def hyperparameters_values(params):
    hyperparameters = hyperparameters_default_values.copy()
    for k, v in params.items():
        if k in hyperparameters:
            hyperparameters[k] = v
    return hyperparameters
