package es.upv.mbda.tfm.zygarde;

import java.io.IOException;
import java.net.URISyntaxException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.Random;
import java.util.TreeSet;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import ca.ubc.cs.beta.aeatk.algorithmrunresult.AlgorithmRunResult;
import ca.ubc.cs.beta.aeatk.parameterconfigurationspace.ParameterConfiguration;
import es.upv.mbda.tfm.zygarde.result.AlgorithmResult;
import es.upv.mbda.tfm.zygarde.result.ModelResult;
import es.upv.mbda.tfm.zygarde.schema.Algorithm;
import es.upv.mbda.tfm.zygarde.schema.Hyperparameter;
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
		List<AlgorithmRunResult> smacResults = new ArrayList<>(0);
		
		try {
			String[] cmdArgs = buildSmacCmdArgs();
			
			SmacExecutor smac = new SmacExecutor();
			smacResults = smac.runSmac(cmdArgs);
		} catch (IOException ioe) {
			LOGGER.error("IOException during composition of SMAC CMD arguments: " + ioe.getMessage(), ioe);
		}
		
		AlgorithmResult aggregateResult = transformSmacAlgorithmResults(smacResults);
		
		lifecycleExecuteOnFinishTask((TreeSet<ModelResult>) aggregateResult.getResults());
		
		LOGGER.info(String.format("Algorithm: %s\tBest precision: %1.4f",
				aggregateResult.getAlgorithm(), aggregateResult.getBestPrecision()));
		
		return aggregateResult;
	}
	
	private String[] buildSmacCmdArgs() throws IOException {
		int seed = new Random().nextInt(32768);
		
		Map<String, String> argsMap = new HashMap<>();
		argsMap.put("scenario-file", getScenarioPath().toString());
		argsMap.put("pcs-file", writeParamsFile(seed).toString());
		argsMap.put("numberOfRunsLimit", String.valueOf(getNumberOfRunsLimit()));
		argsMap.put("rungroup", String.format("%s-%d", method.getAlgorithm(), seed));
		argsMap.put("seed", String.valueOf(seed));
		
		String[] argsArray = new String[argsMap.size() * 2 + 1];
		int n = 0;
		argsArray[n++] = "smac";
		for (Map.Entry<String, String> arg : argsMap.entrySet()) {
			argsArray[n] = "--" + arg.getKey();
			argsArray[n+1] = arg.getValue();
			n += 2;
		}
		
		return Arrays.copyOfRange(argsArray, 1, argsArray.length);
	}
	
	private Path getScenarioPath() {
		Path scenarioPath;
		try {
			scenarioPath = Paths.get(getClass().getClassLoader().getResource("smac/scenario.txt").toURI());
		} catch (URISyntaxException urise) {
			LOGGER.warn(urise.getMessage());
			scenarioPath = Paths.get("smac", "scenario.txt");
		}
		return scenarioPath;
	}
	
	private Path writeParamsFile(int seed) throws IOException {
		Path paramsPath = Paths.get(System.getProperty("user.dir"), "smac", "params",
				String.format("params-%d.pcs", seed));
		
		final String CATEGORICAL_PARAM = " categorical ";
		List<String> paramLines = new ArrayList<>(method.getHyperparameters().size());
		StringBuilder line;
		for (Hyperparameter<?> hp : method.getHyperparameters()) {
			line = new StringBuilder(hp.getParam()).append(CATEGORICAL_PARAM).append('{');
			for (Object pv : hp.getValues()) {
				line.append(String.format(" %s ,", pv.toString()));
			}
			line.setCharAt(line.length() - 1, '}');
			line.append(String.format(" [%s]", hp.getValues().get(0).toString()));
			paramLines.add(line.toString());
		}
		
		Files.write(paramsPath, paramLines, StandardCharsets.UTF_8);
		return paramsPath;
	}
	
	private int getNumberOfRunsLimit() {
		int numCombinations = 1;
		for (Hyperparameter<?> hp : method.getHyperparameters()) {
			numCombinations *= hp.getValues().size();
		}
		return numCombinations;
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
		return new ModelResult(-runResult.getQuality(), //Math.abs(runResult.getQuality()),
				algorithm, hyperparameters);	// FIXME
	}
	
	private void lifecycleExecuteOnFinishTask(TreeSet<ModelResult> results) {
		Iterator<ModelResult> it = results.descendingIterator();
		while (it.hasNext()) {
			lifecycle.onFinishTask(it.next());
		}
	}
	
	private static final Logger LOGGER = LoggerFactory.getLogger(
			BayesianOptimizationMethodExecutor.class);
}
