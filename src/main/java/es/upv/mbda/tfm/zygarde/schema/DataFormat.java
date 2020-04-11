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
 * @class es.upvm.bda.tfm.zygarde.schema.DataFormat
 */
public enum DataFormat {
	
	LIB_SVM("libsvm");
	
	public final String name;
	private static Map<String, DataFormat> nameValues;
	
	private DataFormat(String name) {
		this.name = name;
	}
	
	static {
		nameValues = new HashMap<>();
		for (DataFormat enumValue : values()) {
			nameValues.put(enumValue.name, enumValue);
		}
	}
	
	public static DataFormat forName(String label) {
		return nameValues.get(label);
	}
	
	@Override
	public String toString() {
		return this.name;
	}
}
