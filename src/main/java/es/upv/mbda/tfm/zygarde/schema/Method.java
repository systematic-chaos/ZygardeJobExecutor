package es.upv.mbda.tfm.zygarde.schema;

import java.util.List;

/**
 * @author thanatos
 * @class es.upv.mbda.tfm.zygarde.schema.Method
 */
public class Method {
	
	private String algorithm;
	private List<Hyperparameter<?>> hyperparameters;
	
	public String getAlgorithm() {
		return this.algorithm;
	}
	
	public void setAlgorithm(String algorithm) {
		this.algorithm = algorithm;
	}
	
	public List<Hyperparameter<?>> getHyperparameters() {
		return this.hyperparameters;
	}
	
	public void setHyperparameters(List<Hyperparameter<?>> hyperparameters) {
		this.hyperparameters = hyperparameters;
	}
}
