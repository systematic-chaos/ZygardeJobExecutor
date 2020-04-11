package es.upv.mbda.tfm.zygarde;

import java.util.concurrent.Callable;

import es.upv.mbda.tfm.zygarde.result.AlgorithmResult;
import es.upv.mbda.tfm.zygarde.schema.Method;

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
 * @class es.upv.mbda.tfm.zygarde.MethodExecutor
 */
public abstract class MethodExecutor implements Callable<AlgorithmResult> {
	
	protected Method method;
	protected JobLifecycle lifecycle;
	
	@Override
	public AlgorithmResult call() {
		return executeMethod();
	}
	
	abstract public AlgorithmResult executeMethod();
	
	public AlgorithmResult executeMethod(Method method) {
		this.method = method;
		return executeMethod();
	}
}
