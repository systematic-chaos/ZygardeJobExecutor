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
