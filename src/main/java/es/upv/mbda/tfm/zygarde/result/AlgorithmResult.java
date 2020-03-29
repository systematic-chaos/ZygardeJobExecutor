package es.upv.mbda.tfm.zygarde.result;

import java.util.Collection;

import es.upv.mbda.tfm.zygarde.schema.Algorithm;

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
