package es.upv.mbda.tfm.zygarde;

import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.TreeSet;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import ca.ubc.cs.beta.aeatk.algorithmrunresult.AlgorithmRunResult;
import ca.ubc.cs.beta.aeatk.parameterconfigurationspace.ParameterConfiguration;
import es.upv.mbda.tfm.zygarde.result.AlgorithmResult;
import es.upv.mbda.tfm.zygarde.result.ModelResult;
import es.upv.mbda.tfm.zygarde.schema.Algorithm;
import es.upv.mbda.tfm.zygarde.schema.Method;
import es.upv.mbda.tfm.zygarde.smac.SmacExecutor;

/**
 * @author thanatos
 * @class es.upv.mbda.tfm.zygarde.BayesianOptimizationMethodExecutor
 */
public class BayesianOptimizationMethodExecutor extends MethodExecutor {
	
	public BayesianOptimizationMethodExecutor(Method method, JobLifecycle lifecycle) {
		this.method = method;
		this.lifecycle = lifecycle;
	}
	
	public AlgorithmResult executeMethod() {
		String[] cmdArgs = buildSmacCmdArgs();
		
		SmacExecutor smac = new SmacExecutor();
		List<AlgorithmRunResult> smacResults = smac.runFakeSmac(cmdArgs);
		
		AlgorithmResult aggregateResult = transformSmacAlgorithmResults(smacResults);
		
		fakeTask(aggregateResult);
		
		lifecycle.onFinishTask(aggregateResult.getBestResult());
		executeTaskFinishLifecycle((TreeSet<ModelResult>) aggregateResult.getResults());
		
		LOGGER.info(String.format("Algorithm: %s\tBest precision: %1.4f",
				aggregateResult.getAlgorithm(), aggregateResult.getBestPrecision()));
		
		return aggregateResult;
	}
	
	private ModelResult fakeTask() {
		ParameterizedAlgorithmExecutor taskExecutor
			= new ParameterizedAlgorithmExecutor(
					Algorithm.forName(method.getAlgorithm()), new HashMap<>(), lifecycle);
		ModelResult bestResult = taskExecutor.executeAlgorithm();
		return bestResult;
	}
	
	private void fakeTask(AlgorithmResult result) {
		result.addResult(fakeTask());
	}
	
	private String[] buildSmacCmdArgs() {    // FIXME
		return new String[0];
	}
	
	private AlgorithmResult transformSmacAlgorithmResults(List<AlgorithmRunResult> algRunResults) {
		AlgorithmResult algResult = new AlgorithmResult(Algorithm.forName(method.getAlgorithm()));
		for (AlgorithmRunResult runResult : algRunResults) {
			algResult.addResult(runResultToModelResult(algResult.getAlgorithm(), runResult));
		}
		return algResult;
	}
	
	private ModelResult runResultToModelResult(Algorithm algorithm, AlgorithmRunResult runResult) {
		ParameterConfiguration smacParams = runResult.getParameterConfiguration();
		Map<String, String> hyperparameters = new HashMap<>(smacParams.size());
		for (String key : smacParams.keySet()) {
			hyperparameters.put(key, smacParams.get(key));
		}
		return new ModelResult(runResult.getQuality(), algorithm, hyperparameters);
	}
	
	private void executeTaskFinishLifecycle(TreeSet<ModelResult> results) {
		Iterator<ModelResult> it = results.descendingIterator();
		while (it.hasNext()) {
			lifecycle.onFinishTask(it.next());
		}
	}
	
	private static final Logger LOGGER = LoggerFactory.getLogger(
			BayesianOptimizationMethodExecutor.class);
}
