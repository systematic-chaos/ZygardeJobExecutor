package es.upv.mbda.tfm.zygarde;

import java.util.Map;
import java.util.Random;
import java.util.concurrent.Callable;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import es.upv.mbda.tfm.zygarde.result.ModelResult;
import es.upv.mbda.tfm.zygarde.schema.Algorithm;

/**
 * @author thanatos
 * @class es.upv.mbda.tfm.zygarde.ParameterizedAlgorithmExecutor
 */
public class ParameterizedAlgorithmExecutor implements Callable<ModelResult> {
	
	private Algorithm algorithm;
	private Map<String, ?> hyperparameters;
	private JobLifecycle lifecycle;
	
	public ParameterizedAlgorithmExecutor(Algorithm algorithm,
			Map<String, ?> params, JobLifecycle lifecycle) {
		this.algorithm = algorithm;
		this.hyperparameters = params;
		this.lifecycle = lifecycle;
	}
	
	public ModelResult executeAlgorithm() {
		double precision = new Random().nextDouble();
		ModelResult result = new ModelResult(precision, algorithm, hyperparameters);
		LOGGER.info(String.format("%s:\t%1.4f", algorithm, precision));
		return result;
	}
	
	public ModelResult executeAlgorithm(Algorithm algorithm, Map<String, ?> params) {
		this.algorithm = algorithm;
		this.hyperparameters = params;
		return executeAlgorithm();
	}
	
	@Override
	public ModelResult call() {
		ModelResult result = executeAlgorithm();
		lifecycle.onFinishTask(result);
		return result;
	}
	
	private static final Logger LOGGER = LoggerFactory.getLogger(ParameterizedAlgorithmExecutor.class);

}
