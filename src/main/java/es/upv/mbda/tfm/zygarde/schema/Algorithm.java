package es.upv.mbda.tfm.zygarde.schema;

import java.util.HashMap;
import java.util.Map;

/**
 * Zygarde: Platform for reactive training of models in the cloud
 * Master in Big Data Analytics
 * Polytechnic University of Valencia
 * 
 * @author		Javier Fernández-Bravo Peñuela
 * @copyright	2020 Ka-tet Corporation. All rights reserved.
 * @license		GPLv3.0
 * @contact		fjfernandezbravo@iti.es
 * 
 * @class es.upv.mbda.tfm.zygarde.schema.Algorithm
 */
public enum Algorithm {
	
	LINEAR_REGRESSION("linear-regression"),
	GLRM("generalized-linear-regression"),
	RANDOM_FOREST_REGRESSION("random-forest-regression"),
	DECISION_TREE_REGRESSION("decision-tree-regression"),
	GBT_REGRESSION("gradient-boosted-tree-regression"),
	LVSM("linear-support-vector-machine"),
	BINOMIAL_LOGISTIC_REGRESSION("binomial-logistic-regression"),
	NAIVE_BAYES("naive-bayes"),
	RANDOM_FOREST_CLASSIFICATION("random-forest-classification"),
	MULTINOMIAL_LOGISTIC_REGRESSION("multinomial-logistic-regression"),
	DECISION_TREE_CLASSIFICATION("decision-tree-classification"),
	GBT_CLASSIFICATION("gradient-boosted-tree-classification"),
	K_MEANS("k-means"),
	GMM("gaussian-mixture-model"),
	MLPC("multilayer-perceptron-classifier"),
	BRANIN("branin");
	
	public final String name;
	private static Map<String, Algorithm> nameValues;
	
	private Algorithm(String name) {
		this.name = name;
	}
	
	static {
		nameValues = new HashMap<>();
		for (Algorithm enumValue : values()) {
			nameValues.put(enumValue.name, enumValue);
		}
	}
	
	public static Algorithm forName(String label) {
		return nameValues.get(label);
	}
	
	@Override
	public String toString() {
		return this.name;
	}
}
