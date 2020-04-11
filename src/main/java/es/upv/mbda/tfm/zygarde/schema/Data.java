package es.upv.mbda.tfm.zygarde.schema;

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
 * @class es.upv.mbda.tfm.zygarde.schema.Data
 */
public class Data {
	
	private String path;
	private String format;
	
	public String getPath() {
		return this.path;
	}
	
	public void setPath(String path) {
		this.path = path;
	}
	
	public String getFormat() {
		return this.format;
	}
	
	public void setFormat(String format) {
		this.format = format;
	}
}
