package es.upv.mbda.tfm.zygarde.schema;

import java.util.List;

import com.fasterxml.jackson.annotation.JsonIgnore;

/**
 * @author thanatos
 * @class es.upv.bmda.tfm.zygarde.schema.ZygardeRequest
 */
public class ZygardeRequest {
	
	private String domain;
	private List<Method> methods;
	private ComputationalResource computationalResources;
	private String emailAddress;
	
	@JsonIgnore
	private String requestId;
	
	public String getDomain() {
		return this.domain;
	}
	
	public void setDomain(String domain) {
		this.domain = domain;
	}
	
	public List<Method> getMethods() {
		return this.methods;
	}
	
	public void setMethods(List<Method> methods) {
		this.methods = methods;
	}
	
	public ComputationalResource getComputationalResources() {
		return this.computationalResources;
	}
	
	public void setComputationalResources(ComputationalResource computationalResources) {
		this.computationalResources = computationalResources;
	}
	
	public String getEmailAddress() {
		return this.emailAddress;
	}
	
	public void setEmailAddress(String emailAddress) {
		this.emailAddress = emailAddress;
	}
	
	public String getRequestId() {
		return this.requestId;
	}
	
	public void setRequestId(String requestId) {
		this.requestId = requestId;
	}
}
