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
 * @class es.upv.mbda.tfm.zygarde.schema.Instance
 */
public class Instance {
	
	private String ec2Instance;
	private List<String> additionalHardware;
	private Integer minInstances;
	private Integer maxInstances;
	
	public String getEc2Instance() {
		return this.ec2Instance;
	}
	
	public void setEc2Instance(String ec2Instance) {
		this.ec2Instance = ec2Instance;
	}
	
	public List<String> getAdditionalHardware() {
		return this.additionalHardware;
	}
	
	public void setAdditionalHardware(List<String> additionalHardware) {
		this.additionalHardware = additionalHardware;
	}
	
	public Integer getMinInstances() {
		return this.minInstances;
	}
	
	public void setMinInstances(Integer minInstances) {
		this.minInstances = minInstances;
	}
	
	public Integer getMaxInstances() {
		return this.maxInstances;
	}
	
	public void setMaxInstances(Integer maxInstances) {
		this.maxInstances = maxInstances;
	}
}
