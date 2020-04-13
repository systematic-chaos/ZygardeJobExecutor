package es.upv.mbda.tfm.zygarde;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;
import java.util.concurrent.TimeUnit;
import java.util.stream.Collectors;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import es.upv.mbda.tfm.zygarde.result.AlgorithmResult;
import es.upv.mbda.tfm.zygarde.result.ModelResult;
import es.upv.mbda.tfm.zygarde.schema.Algorithm;
import es.upv.mbda.tfm.zygarde.schema.Data;
import es.upv.mbda.tfm.zygarde.schema.Hyperparameter;
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
 * @class es.upv.mbda.tfm.zygarde.GridSearchMethodExecutor
 */
public class GridSearchMethodExecutor extends MethodExecutor {
	
	public GridSearchMethodExecutor(String requestId, Method method, Data dataset, JobLifecycle lifecycle) {
		this.requestId = requestId;
		this.method = method;
		this.dataset = dataset;
		this.lifecycle = lifecycle;
	}
	
	public AlgorithmResult executeMethod() {
		List<ParameterizedAlgorithmExecutor> tasks = computeTasks(method);
		
		Algorithm algorithm = Algorithm.forName(method.getAlgorithm());
		AlgorithmResult result = executeParameterizedAlgorithm(algorithm, tasks);
		
		LOGGER.info(String.format("Algorithm: %s\tBest precision: %1.4f",
				result.getAlgorithm(), result.getBestPrecision()));
		return result;
	}
	
	protected List<ParameterizedAlgorithmExecutor> computeTasks(Method method) {
		List<ParameterizedAlgorithmExecutor> tasks;
		Algorithm algorithm = Algorithm.forName(method.getAlgorithm());
		
		if (method.getHyperparameters() != null && !method.getHyperparameters().isEmpty()) {
			tasks = combineParams(method.getHyperparameters())
					.stream()
					.map(paramConfig -> new ParameterizedAlgorithmExecutor(
							algorithm, paramConfig, dataset, requestId, lifecycle))
					.collect(Collectors.toList());
		} else {
			tasks = new ArrayList<>();	// unparameterized algorithm
			tasks.add(new ParameterizedAlgorithmExecutor(
					algorithm, new HashMap<>(), dataset, requestId, lifecycle));
		}
		
		return tasks;
	}
	
	protected AlgorithmResult executeParameterizedAlgorithm(Algorithm algorithm,
			List<ParameterizedAlgorithmExecutor> tasks) {
		AlgorithmResult aggregateResult = new AlgorithmResult(algorithm);
		ExecutorService executor = Executors.newCachedThreadPool();
		
		try {
			List<Future<ModelResult>> taskResults = executor.invokeAll(tasks);
			executor.shutdown();
			if (!executor.awaitTermination(12l, TimeUnit.HOURS)) {
				executor.shutdownNow();
			}
			
			for (Future<ModelResult> fmr : taskResults) {
				aggregateResult.addResult(fmr.get());
			}
		} catch (InterruptedException | ExecutionException e) {
			LOGGER.error("Interrupted exception on algorithm parameterized execution\n"
					+ e.getMessage(), e);
		}
		
		return aggregateResult;
	}
	
	private List<Map<String, ?>> combineParams(List<Hyperparameter<?>> hyperparameters) {
		return combineParams(hyperparameters, 0, new int[hyperparameters.size()],
				new ArrayList<>());
	}
	
	@SuppressWarnings("unused")
	private List<Map<String, ?>> combineParams(List<Hyperparameter<?>> hyperparameters,
			int dimension, int[] indexes) {
		List<Map<String, ?>> paramConfigurations = new ArrayList<>();
		Hyperparameter<?> param = hyperparameters.get(dimension);
		int numValues = param.getValues().size();
		
		for (int v = 0; v < numValues; v++) {
			indexes[dimension] = v;
			if (dimension < hyperparameters.size() - 1) {
				paramConfigurations.addAll(combineParams(hyperparameters, dimension + 1, indexes));
			} else {
				paramConfigurations.add(buildParamConfig(hyperparameters, indexes));
			}
		}
		
		return paramConfigurations;
	}
	
	private List<Map<String, ?>> combineParams(List<Hyperparameter<?>> hyperparameters,
			int dimension, int[] indexes, List<Map<String, ?>> paramConfigurations) {
		Hyperparameter<?> param = hyperparameters.get(dimension);
		int numValues = param.getValues().size();
		
		for (int v = 0; v < numValues; v++) {
			indexes[dimension] = v;
			if (dimension < hyperparameters.size() - 1) {
				combineParams(hyperparameters, dimension + 1, indexes, paramConfigurations);
			} else {
				paramConfigurations.add(buildParamConfig(hyperparameters, indexes));
			}
		}
		
		return paramConfigurations;
	}
	
	private Map<String, ?> buildParamConfig(List<Hyperparameter<?>> hyperparameters, int[] indexes) {
		Map<String, Object> paramConfig = new HashMap<>();
		Hyperparameter<?> param;
		
		for (int n = 0; n < indexes.length; n++) {
			param = hyperparameters.get(n);
			paramConfig.put(param.getParam(), param.getValues().get(indexes[n]));
		}
		
		return paramConfig;
	}
	
	private static final Logger LOGGER = LoggerFactory.getLogger(
			GridSearchMethodExecutor.class);
}
