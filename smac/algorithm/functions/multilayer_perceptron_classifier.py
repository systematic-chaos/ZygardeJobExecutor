'''
algorithm/functions/multilayer_perceptron_classifier
Classifier trainer based on the Multilayer Perceptron.
Multilayer perceptron classifier (MLPC) is a classifier based on the feedforward
artificial neural network. MLPC consists of multiple layers of nodes. Each layer
is fully connected to the next layer in the network. Nodes in the input layer
represent the input data. All other nodes map inputs to outputs by a linear combination
of the inputs with the node's weights `w` and bias `b` and applygin an activation function.
MLPC employs backpropagation for learning the model.
Each layer has sigmoid activation function, output layer has softmax.
Number of inputs has to be equal to the size of vectors.
Number of outputs has to be equal to the total number of labels.

Zygarde: Platform for reactive training of models in the cloud
Master in Big Data Analytics
Polytechnic University of Valencia

@author:    Javier Fernández-Bravo Peñuela
@copyright: 2020 Ka-tet Corporation. All rights reserved.
@license:   GPLv3.0
@contact:   fjfernandezbravo@iti.es
'''

from pyspark.ml.classification import MultilayerPerceptronClassifier
from pyspark.ml.evaluation import MulticlassClassificationEvaluator

hyperparameters_default_values = {
    'maxIter': 100,
    'blockSize': 128,
    'inputLayerWidth': 4,
    'numHiddenLayers': 3,
    'hiddenLayersWidth': 5,
    'outputLayerWidth': 3,
    'featuresCol': 'features',
    'labelCol': 'label',
    'predictionCol': 'prediction'
}

def multilayer_perceptron_classifier(spark, data, hyperparameters):
    
    # Split the data into training and test sets
    (training_data, test_data) = data.randomSplit([0.8, 0.2])

    # Specify layers for the neural network: input (features),
    # intermediate (hidden) and output (classes) layers
    layers = [hyperparameters['inputLayerWidth']] + \
            [hyperparameters['hiddenLayersWidth']] * hyperparameters['numHiddenLayers'] + \
            [hyperparameters['outputLayerWidth']]
    
    # Create the classifier and set its parameters
    mlp_classifier = MultilayerPerceptronClassifier(layers=layers,
                                                    maxIter=hyperparameters['maxIter'],
                                                    blockSize=hyperparameters['blockSize'])
    
    # Train the model
    mlpc_model = mlp_classifier.fit(training_data)

    # Make predictions
    predictions = mlpc_model.transform(test_data)\
        .select(hyperparameters['predictionCol'], hyperparameters['labelCol'])

    # Compute F1 score on the test ste
    evaluator = MulticlassClassificationEvaluator(metricName='f1')
    f1_score = evaluator.evaluate(predictions)

    return f1_score, mlpc_model

def multilayer_perceptron_classifier_func(spark, params={}, data=None):
    hyperparams = hyperparameters_values(params)

    (score, model) = multilayer_perceptron_classifier(spark, data, hyperparams)
    return score, model

def hyperparameters_values(params):
    hyperparameters = hyperparameters_default_values.copy()
    for k, v in params.items():
        if k in hyperparameters:
            hyperparameters[k] = v
    return hyperparameters
