package es.upv.mbda.tfm.zygarde.result;

import java.util.Map;

import es.upv.mbda.tfm.zygarde.schema.Algorithm;

public class ModelResult implements Comparable<ModelResult> {
	
	private double precision;
	private Algorithm algorithm;
	private Map<String, ?> hyperparameters;
	
	public ModelResult(double precision, Algorithm algorithm, Map<String, ?> hyperparameters) {
		this.setPrecision(precision);
		this.setAlgorithm(algorithm);
		this.setHyperparameters(hyperparameters);
	}
	
	public double getPrecision() {
		return this.precision;
	}
	
	public void setPrecision(double precision) {
		this.precision = precision;
	}
	
	public Algorithm getAlgorithm() {
		return this.algorithm;
	}
	
	public void setAlgorithm(Algorithm algorithm) {
		this.algorithm = algorithm;
	}
	
	public Map<String, ?> getHyperparameters() {
		return this.hyperparameters;
	}
	
	public void setHyperparameters(Map<String, ?> hyperparameters) {
		this.hyperparameters = hyperparameters;
	}
	
	@Override
	public String toString() {
		StringBuilder str = new StringBuilder(String.format("%s:\t%1.4f\t", algorithm, precision));
		for (Map.Entry<String, ?> hp : hyperparameters.entrySet()) {
			str.append(String.format("    %s: ", hp.getKey()) + hp.getValue());
		}
		return str.toString();
	}
	
	@Override
	public int compareTo(ModelResult other) {
		return other != null ?
				Double.compare(this.getPrecision(), other.getPrecision()) : 1;
	}
}
