'''
algorithm/evaluation
Metrics for evaluating a model on a test dataset

Zygarde: Platform for reactive training models in the cloud
Master in Big Data Analytics
Polytechnic University of Valencia

@author:    Javier Fernández-Bravo Peñuela
@copyright: 2020 Ka-tet Corporation. All rights reserved.
@license:   GPLv3.0
@contact:   fjfernandezbravo@iti.es
'''

import numpy as np
from math import sqrt
from pyspark.ml.feature import StringIndexer
from pyspark.ml.evaluation import BinaryClassificationEvaluator
from pyspark.sql.functions import col
from sklearn.metrics import confusion_matrix

# Model accuracy
def accuracy(tp, tn, fp, fn):
    return float(tp + tn) / float(tp + tn + fp + fn)

# Sensivity / Recall
def recall(tp, fn):
    return float(tp) / (tp + fn)

# Specificity
def spec(tn, fp):
    return float(tn) / (tn + fp)

# Precision / PPV
def precision(tp, fp):
    return float(tp) / float(tp + fp)

# F-measure
def fscore(tp, tn, fp, fn):
    rc = recall(tp, fn)
    p = precision(tp, fp)
    return 2 * rc * p / (rc + p)

# Matthew's Correlation Coefficient for binomial classification
def mcc(tp, tn, fp, fn):
    return (tp * tn - fp * fn) / sqrt((tp + fp) * (tp + fn) * (fp + tn) * (tn + fn))

# Cohen's kappa coefficient
def cohen_kappa(tp, tn, fp, fn):
    return kappa(tp, tn, fp, fn)

def kappa(tp, tn, fp, fn):
    N = tp + tn + fp + fn
    p_o = float(tp + tn) / N    # Probability observed
    p_e = float(((tn + fp) * (tn + fn)) + ((fn + tp) * (fp + tp))) / (N * N)    # Probability expected
    k = float(p_o - p_e) / (1 - p_e)    # Cohen's kappa coefficient
    return k

# Mean Square Error (MSE)
def mse(real, estimation):
    deviation = real - estimation
    return 0.5 * np.dot(deviation, deviation)

# Root Mean Square Error (RMSE)
def rmse(real, estimation):
    deviation = real - estimation
    return np.sqrt(2 * np.dot(deviation, deviation) / len(deviation))

def confusion_matrix_rates(predictions):
    labels_df = predictions.withColumn('category', col('label'))
    preds_df = predictions.withColumn('category', col('prediction'))
    indexer = StringIndexer(inputCol='category', outputCol='indexedCategory').fit(labels_df)
    labels_ind = np.array(indexer.transform(labels_df).select('indexedCategory').collect()).ravel()
    preds_ind = np.array(indexer.transform(preds_df).select('indexedCategory').collect()).ravel()

    conf_mat = confusion_matrix(labels_ind, preds_ind, labels=np.unique(labels_ind))

    if conf_mat.shape[0] == 2:
        (tn, fp, fn, tp) = conf_mat.ravel()
        return tp, tn, fp, fn
    else:
        return conf_mat

# Area under the ROC curve
def auroc(predictions):
    return BinaryClassificationEvaluator(metricName='areaUnderROC').evaluate(predictions)

# Area under the PR curve
def aupr(predictions):
    return BinaryClassificationEvaluator(metricName='areaUnderPR').evaluate(predictions)
