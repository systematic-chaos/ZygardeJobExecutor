package es.upv.mbda.tfm.zygarde;

import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.Arrays;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.concurrent.Callable;
import java.util.stream.Collectors;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import es.upv.mbda.tfm.zygarde.result.ModelResult;
import es.upv.mbda.tfm.zygarde.schema.Algorithm;
import es.upv.mbda.tfm.zygarde.schema.Data;

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
 * @class es.upv.mbda.tfm.zygarde.ParameterizedAlgorithmExecutor
 */
public class ParameterizedAlgorithmExecutor implements Callable<ModelResult> {
	
	private Algorithm algorithm;
	private Map<String, ?> hyperparameters;
	private Data dataset;
	private String requestId;
	private JobLifecycle lifecycle;
	
	public ParameterizedAlgorithmExecutor(Algorithm algorithm, Map<String, ?> params,
			Data dataset, String requestId, JobLifecycle lifecycle) {
		this.algorithm = algorithm;
		this.hyperparameters = params;
		this.dataset = dataset;
		this.requestId = requestId;
		this.lifecycle = lifecycle;
	}
	
	public ModelResult executeAlgorithm() {
		double precision = executeParameterizedAlgorithm();
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
	
	private double executeParameterizedAlgorithm() {
		double precision = 0.;
		final String SUCCESS_PREFIX = "Result for Zygarde: SUCCESS\t";
		ProcessBuilder procBuilder = new ProcessBuilder();
		procBuilder.directory(new File(System.getProperty("user.dir")));
		procBuilder.command(composeCmdArgs());
		LOGGER.info(String.join(" ", composeCmdArgs()));
		
		BufferedReader procStdOutput = null;
		BufferedReader procErrOutput = null;
		try {
			Process p = procBuilder.start();
			procStdOutput = new BufferedReader(new InputStreamReader(p.getInputStream()));
			procErrOutput = new BufferedReader(new InputStreamReader(p.getErrorStream()));
			int exitCode = p.waitFor();
			
			List<String> procResultOutput = procStdOutput.lines().collect(Collectors.toList());
			if (exitCode == 0) {
				Optional<String> resultOutput = procResultOutput.stream()
						.filter(line ->  line.startsWith(SUCCESS_PREFIX)).findFirst();
				if (resultOutput.isPresent()) {
					LOGGER.debug(resultOutput.get());
					precision = Double.parseDouble(resultOutput.get().substring(SUCCESS_PREFIX.length()));
				} else {
					procResultOutput.forEach(LOGGER::error);
					procErrOutput.lines().forEach(LOGGER::warn);
				}
			} else {
				LOGGER.error("Exit code: " + exitCode);
			}
		} catch (IOException | InterruptedException | NumberFormatException | NullPointerException e) {
			LOGGER.error("Exception launching subprocess: " + e.getMessage());
		} finally {
			try {
				if (procStdOutput != null) {
					procStdOutput.close();
				}
				if (procErrOutput != null) {
					procErrOutput.close();
				}
			} catch (IOException ioe) {
				LOGGER.error("IOException closing stream resources: " + ioe.getMessage());
			}
		}
		
		return precision;
	}
	
	private String[] composeCmdArgs() {
		final String EXEC = "smac/algorithm_zygarde_wrapper.py";
		
		int i = 0;
		String[] args = new String[(hyperparameters.size() + 4) * 2 + 1];
		args[i++] = EXEC;
		
		args[i++] = "--" + "id";
		args[i++] = requestId;
		
		args[i++] = "--" + "algorithm";
		args[i++] = algorithm.toString();
		
		if (dataset != null) {
			args[i++] = "--" + "dataset";
			args[i++] = dataset.getPath();
			
			if (dataset.getFormat() != null) {
				args[i++] = "--dataFormat";
				args[i++] = dataset.getFormat();
			}
		}
		
		for (Map.Entry<String, ?> param : hyperparameters.entrySet()) {
			args[i] = "-" + param.getKey();
			args[i+1] = param.getValue().toString();
			i += 2;
		}
		
		return Arrays.copyOf(args, i);
	}
	
	private static final Logger LOGGER = LoggerFactory.getLogger(ParameterizedAlgorithmExecutor.class);

}
