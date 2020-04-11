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
 * @class		es.upv.mbda.tfm.zygarde.schema.ParameterSearch
 */
public enum ParameterSearch {
	
	GRID("grid"),
	RANDOM("random"),
	BAYESIAN_OPTIMIZATION("bayesian-optimization");
	
	public final String name;
	private static Map<String, ParameterSearch> nameValues;
	
	private ParameterSearch(String name) {
		this.name = name;
	}
	
	static {
		nameValues = new HashMap<>();
		for (ParameterSearch enumValue : values()) {
			nameValues.put(enumValue.name, enumValue);
		}
	}
	
	public static ParameterSearch forName(String label) {
		return nameValues.get(label);
	}
	
	@Override
	public String toString() {
		return this.name;
	}
}
