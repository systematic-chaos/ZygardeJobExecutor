package es.upv.mbda.tfm.zygarde.schema;

import java.util.HashMap;
import java.util.Map;

/**
 * @author thanatos
 * @class es.upv.mbda.tfm.zygarde.schema.AdditionalHardware
 */
public enum AdditionalHardware {
	
	GPU("GPU");
	
	public final String name;
	private static Map<String, AdditionalHardware> nameValues;
	
	private AdditionalHardware(String name) {
		this.name = name;
	}
	
	static {
		nameValues = new HashMap<>();
		for (AdditionalHardware enumValue : values()) {
			nameValues.put(enumValue.name, enumValue);
		}
	}
	
	public static AdditionalHardware forName(String label) {
		return nameValues.get(label);
	}
	
	@Override
	public String toString() {
		return this.name;
	}
}
