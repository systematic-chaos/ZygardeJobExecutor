package es.upv.mbda.tfm.zygarde.schema;

import java.util.List;

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
 * @class es.upv.mbda.tfm.zygarde.schema.Hyperparameter
 * @param <T> String | Integer
 */
public class Hyperparameter<T> {
	
	private String param;
	private List<T> values;
	
	public String getParam() {
		return this.param;
	}
	
	public void setParam(String param) {
		this.param = param;
	}
	
	public List<T> getValues() {
		return this.values;
	}
	
	public void setValues(List<T> values) {
		this.values = values;
	}
}
