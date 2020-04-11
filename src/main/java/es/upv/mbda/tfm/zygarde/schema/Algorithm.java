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
	
	DECISION_TREE("decision-tree"),
	SVM("svm"),
	K_MEANS("k-means"),
	NEURAL_NETWORK("neural-network"),
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
