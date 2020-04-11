package es.upv.mbda.tfm.zygarde.schema;

import java.util.List;

/**
 * Zygarde: Platform for reactive training of models in the cloud.
 * Master in Big Data Analytics
 * Polytechnic University of Valencia
 * 
 * @author		Javier Fernández-Bravo Peñuela
 * @copyright	2020 Ka-tet Corporation. All rights reserved.
 * @license		GPLv3.0
 * @contact		fjfernandezbravo@iti.es
 * 
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
