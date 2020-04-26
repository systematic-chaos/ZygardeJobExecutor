'''
algorithm/functions/classification/

Zygarde: Platform for reactive training of models in the cloud
Master in Big Data Analytics
Polytechnic University of Valencia

@author:    Javier Fernández-Bravo Peñuela
@copyright: 2020 Ka-tet Corporation. All rights reserved.
@license:   GPLv3.0
@contact:   fjfernandezbravo@iti.es
'''

from .binomial.gradient_boosted_tree_classification import gradient_boosted_tree_classification_func
from .binomial.linear_support_vector_machine import linear_support_vector_machine_func
from .binomial.logistic_regression import logistic_regression_func as binomial_logistic_regression_func

from .multinomial.decision_tree_classification import decision_tree_classification_func
from .multinomial.multilayer_perceptron_classifier import multilayer_perceptron_classifier_func
from .multinomial.logistic_regression import logistic_regression_func as multinomial_logistic_regression_func
from .multinomial.naive_bayes import naive_bayes_func
from .multinomial.random_forest_classification import random_forest_classification_func
