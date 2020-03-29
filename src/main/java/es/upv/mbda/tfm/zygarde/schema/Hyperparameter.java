package es.upv.mbda.tfm.zygarde.schema;

import java.util.List;

/**
 * @author thanatos
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
