package es.upv.mbda.tfm.zygarde.result;

import java.util.Collection;

import es.upv.mbda.tfm.zygarde.schema.Algorithm;

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
 * @class es.upv.mbda.tfm.zygarde.result.AlgorithmResult
 */
public class AlgorithmResult extends Result {
	
	private Algorithm algorithm;
	
	public AlgorithmResult(Algorithm algorithm) {
		this.setAlgorithm(algorithm);
	}
	
	public AlgorithmResult(Algorithm algorithm, Collection<ModelResult> results) {
		super(results);
		this.setAlgorithm(algorithm);
	}
	
	public Algorithm getAlgorithm() {
		return this.algorithm;
	}
	
	public void setAlgorithm(Algorithm algorithm) {
		this.algorithm = algorithm;
	}
}
