'''
decision_tree_regression -- Regression: Decision Tree regressor

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
from pyspark.ml.regression import DecisionTreeRegressor
from pyspark.ml.feature import VectorIndexer
from pyspark.ml.evaluation import RegressionEvaluator

from ..aux_functions import hyperparameters_values

hyperparameters_default_values = {
    'maxDepth': 5,
    'maxCategories': 4
}

def decision_tree_regression(spark, data, hyperparameters):
    
    # Automatically identify categorical features and index them
    # We specify maxCategories so features with > 4 distinct values are managed as continuous
    feature_indexer = VectorIndexer(maxCategories=hyperparameters['maxCategories'],
                                    inputCol=hyperparameters['featuresCol'],
                                    outputCol='indexedFeatures').fit(data)
    hyperparameters['featuresCol'] = 'indexedFeatures'

    # Split the data into training and test sets
    (training_data, test_data) = data.randomSplit((0.7, 0.3))

    # Train a Decision Tree Regressor model
    dt = DecisionTreeRegressor(maxDepth=hyperparameters['maxDepth'],
                            featuresCol=hyperparameters['featuresCol'])

    # Chain indexer and tree in a Pipeline
    pipeline = Pipeline(stages=[feature_indexer, dt])

    # Train model; this also runs the indexer
    pipeline_model = pipeline.fit(training_data)

    # Make predictions
    predictions = pipeline_model.transform(test_data)

    # Select predictions and compute test error
    evaluator = RegressionEvaluator(metricName='rmse',
                                    labelCol=hyperparameters['labelCol'],
                                    predictionCol=hyperparameters['predictionCol'])
    rmse_score = evaluator.evaluate(predictions)

    dt_model = pipeline_model.stages[1]
    return rmse_score, dt_model

def decision_tree_regression_func(spark, params={}, data=None):
    hyperparams = hyperparameters_values(params, hyperparameters_default_values)

    (score, model) = decision_tree_regression(spark, data, hyperparams)
    return -score, model
