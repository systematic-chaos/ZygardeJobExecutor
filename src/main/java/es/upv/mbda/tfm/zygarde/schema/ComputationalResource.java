package es.upv.mbda.tfm.zygarde.schema;

import java.util.List;

/**
 * @author thanatos
 * @class es.upv.mbda.tfm.zygarde.schema.ComputationalResource
 */
public class ComputationalResource {
	
	private List<Instance> instances;
	private Integer minTotalInstances;
	private Integer maxTotalInstances;
	
	public List<Instance> getInstances() {
		return this.instances;
	}
	
	public void setInstances(List<Instance> instances) {
		this.instances = instances;
	}
	
	public Integer getMinTotalInstances() {
		return this.minTotalInstances;
	}
	
	public void setMinTotalInstances(Integer minTotalInstances) {
		this.minTotalInstances = minTotalInstances;
	}
	
	public Integer getMaxTotalInstances() {
		return this.maxTotalInstances;
	}
	
	public void setMaxTotalInstances(Integer maxTotalInstances) {
		this.maxTotalInstances = maxTotalInstances;
	}
}
