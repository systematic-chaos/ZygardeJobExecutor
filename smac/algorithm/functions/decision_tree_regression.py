'''
algorithm/functions/decision_tree_regression -- Decision Tree regression
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

hyperparameters_default_values = {
    'maxDepth': 5,
    'maxCategories': 4,
    'featuresCol': 'features',
    'labelCol': 'label',
    'predictionCol': 'prediction'
}

def decision_tree_regression(spark, data, hyperparameters):
    
    # Automatically identify categorical features and index them
    # We specify maxCategories so features with > 4 distinct values are managed as continuous
    feature_indexer = VectorIndexer(inputCol=hyperparameters['featuresCol'], outputCol='indexedFeatures',
                                    maxCategories=hyperparameters['maxCategories']).fit(data)
    hyperparameters['featuresCol'] = 'indexedFeatures'

    # Split the data into training and test sets (30% held out for testing)
    (training_data, test_data) = data.randomSplit([0.7, 0.3])

    # Train a Decision Tree Regressor model
    dt = DecisionTreeRegressor(maxDepth=hyperparameters['maxDepth'],
            featuresCol=hyperparameters['featuresCol'])

    # Chain indexer and tree in a Pipeline
    pipeline = Pipeline(stages=[feature_indexer, dt])

    # Train model; this also runs the indexer
    model = pipeline.fit(training_data)

    # Make predictions
    predictions = model.transform(test_data)

    # Select predictions and compute test error
    evaluator = RegressionEvaluator(metricName='rmse',
        labelCol=hyperparameters['labelCol'], predictionCol=hyperparameters['predictionCol'])
    rmse_score = evaluator.evaluate(predictions)

    dt_model = model.stages[1]
    return rmse_score, dt_model

def decision_tree_regression_func(spark, params={}, data=None):
    hyperparams = hyperparameters_values(params)

    (score, model) = decision_tree_regression(spark, data, hyperparams)
    return -score, model

def hyperparameters_values(params):
    hyperparameters = hyperparameters_default_values.copy()
    for k, v in params.items():
        if k in hyperparameters:
            hyperparameters[k] = v
    return hyperparameters
