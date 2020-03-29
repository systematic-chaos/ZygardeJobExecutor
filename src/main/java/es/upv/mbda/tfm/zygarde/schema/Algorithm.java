package es.upv.mbda.tfm.zygarde.schema;

import java.util.HashMap;
import java.util.Map;

/**
 * @author thanatos
 * @class es.upv.mbda.tfm.zygarde.schema.Algorithm
 */
public enum Algorithm {
	
	DECISION_TREE("decision-tree"),
	SVM("svm"),
	K_MEANS("k-means"),
	NEURAL_NETWORK("neural-network");
	
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
