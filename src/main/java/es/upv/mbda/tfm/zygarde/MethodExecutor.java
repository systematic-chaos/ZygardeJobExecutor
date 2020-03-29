package es.upv.mbda.tfm.zygarde;

import java.util.concurrent.Callable;

import es.upv.mbda.tfm.zygarde.result.AlgorithmResult;
import es.upv.mbda.tfm.zygarde.schema.Method;

/**
 * @author thanatos
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
