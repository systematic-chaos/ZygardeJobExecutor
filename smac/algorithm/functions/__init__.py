'''
algorithm/functions/

Zygarde: Platform for reactive training of models in the cloud
Master in Big Data Analytics
Polytechnic University of Valencia

@author:    Javier Fernández-Bravo Peñuela
@copyright: 2020 Ka-tet Corporation. All rights reserved.
@license:   GPLv3.0
@contact:   fjfernandezbravo@iti.es
'''

from .misc.branin import branin_func as branin

from .classification import gradient_boosted_tree_classification_func as gradient_boosted_tree_classification
from .classification import linear_support_vector_machine_func as linear_support_vector_machine
from .classification import binomial_logistic_regression_func as binomial_logistic_regression
from .classification import decision_tree_classification_func as decision_tree_classification
from .classification import multilayer_perceptron_classifier_func as multilayer_perceptron_classifier
from .classification import multinomial_logistic_regression_func as multinomial_logistic_regression
from .classification import naive_bayes_func as naive_bayes
from .classification import random_forest_classification_func as random_forest_classification

from .regression import linear_regression_func as linear_regression
from .regression import random_forest_regression_func as random_forest_regression
from .regression import generalized_linear_regression_func as generalized_linear_regression
from .regression import decision_tree_regression_func as decision_tree_regression
from .regression import gradient_boosted_tree_regression_func as gradient_boosted_tree_regression

from .clustering import k_means_func as k_means
from .clustering import gaussian_mixture_model_func as gaussian_mixture_model
