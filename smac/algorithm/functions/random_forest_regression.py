'''
algorithm/random_forest_regression -- Random forest regression.
Random forests are a popular family of classification and regression methods.
Random forests are ensembles of decision trees. Random forests combine many decision trees
for binary and multiclass classification and for regression, using both continuous and
categorical features.

Zygarde: Platform for reactive training of models in the cloud
Master in Big Data Analytics
Polytechnic University of Valencia

@author:    Javier Fernández-Bravo Peñuela
@copyright: 2020 Ka-tet Corporation. All rights reserved.
@license:   GPLv3.0
@contact:   fjfernandezbravo@iti.es
'''

from pyspark.ml import Pipeline
from pyspark.ml.regression import RandomForestRegressor
from pyspark.ml.feature import VectorIndexer
from pyspark.ml.evaluation import RegressionEvaluator

hyperparameters_default_values = {
    'numTrees': 20,
    'maxDepth': 5,
    'seed': None,
    'maxCategories': 4,
    'featuresCol': 'features',
    'labelCol': 'label',
    'predictionCol': 'prediction'
}

def random_forest_regression(spark, data, hyperparameters):
    
    # Automatically identify categorical features, and index them.
    # Set maxCategories so features with > 4 distinct values are treated as continuous.
    feature_indexer = VectorIndexer(inputCol=hyperparameters['featuresCol'],\
        outputCol='indexedFeatures', maxCategories=hyperparameters['maxCategories']).fit(data)
    hyperparameters['featuresCol'] = 'indexedFeatures'
    
    # Split the data into training and test sets (30% held out for testing)
    (training_data, test_data) = data.randomSplit([0.7, 0.3])

    # Train a RandomForest model
    rf = RandomForestRegressor(numTrees=hyperparameters['numTrees'],
        maxDepth=hyperparameters['maxDepth'],
        seed=hyperparameters['seed'],
        labelCol=hyperparameters['labelCol'],
        featuresCol=hyperparameters['featuresCol'])
    
    # Chain vector indexer and random forest regression in a Pipeline
    pipeline = Pipeline(stages=[feature_indexer, rf])

    # Train model; this also runs the indexer
    model = pipeline.fit(training_data)

    # Make predictions
    predictions = model.transform(test_data)

    # Select (prediction, true label) and compute test error
    evaluator = RegressionEvaluator(labelCol=hyperparameters['labelCol'],\
        predictionCol=hyperparameters['predictionCol'], metricName='rmse')
    rmse = evaluator.evaluate(predictions)

    rf_model = model.stages[1]
    return rmse, rf_model

def random_forest_regression_func(spark, params={}, data=None):
    hyperparams = hyperparameters_values(params)
    
    (rmse, model) = random_forest_regression(spark, data, hyperparams)
    return -rmse, model

def hyperparameters_values(params):
    hyperparameters = hyperparameters_default_values.copy()
    for k, v in params.items():
        if k in hyperparameters:
            hyperparameters[k] = v
    return hyperparameters
