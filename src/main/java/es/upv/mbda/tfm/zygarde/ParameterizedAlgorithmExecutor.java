package es.upv.mbda.tfm.zygarde;

import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.Arrays;
import java.util.Map;
import java.util.concurrent.Callable;

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
	private JobLifecycle lifecycle;
	
	public ParameterizedAlgorithmExecutor(Algorithm algorithm,
			Map<String, ?> params, Data dataset, JobLifecycle lifecycle) {
		this.algorithm = algorithm;
		this.hyperparameters = params;
		this.dataset = dataset;
		this.lifecycle = lifecycle;
	}
	
	public ModelResult executeAlgorithm() {
		double precision = executeParameterizedAlgorithm(algorithm, hyperparameters, dataset);
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
	
	private double executeParameterizedAlgorithm(Algorithm alg, Map<String, ?> params, Data dataset) {
		double precision = 0.;
		final String SUCCESS_PREFIX = "Result for Zygarde: SUCCESS\t";
		ProcessBuilder procBuilder = new ProcessBuilder();
		procBuilder.directory(new File(System.getProperty("user.dir")));
		procBuilder.command(composeCmdArgs(alg.toString(), params, dataset));
		
		BufferedReader procStdOutput = null;
		BufferedReader procErrOutput = null;
		try {
			Process p = procBuilder.start();
			procStdOutput = new BufferedReader(new InputStreamReader(p.getInputStream()));
			procErrOutput = new BufferedReader(new InputStreamReader(p.getErrorStream()));
			int exitCode = p.waitFor();
			
			String resultOutput = procStdOutput.readLine();
			if (exitCode == 0) {
				if (resultOutput.startsWith(SUCCESS_PREFIX)) {
					LOGGER.debug(resultOutput);
					precision = Double.parseDouble(resultOutput.substring(SUCCESS_PREFIX.length()));
				} else {
					LOGGER.error(resultOutput);
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
	
	private String[] composeCmdArgs(String alg, Map<String, ?> params, Data dataset) {
		final String EXEC = "smac/algorithm_zygarde_wrapper.py";
		
		int i = 0;
		String[] args = new String[params.size() * 2 + 7];
		args[i++] = EXEC;
		
		args[i++] = "--" + "algorithm";
		args[i++] = alg;
		
		if (dataset != null) {
			args[i++] = "--" + "dataset";
			args[i++] = dataset.getPath();
			
			if (dataset.getFormat() != null) {
				args[i++] = "--dataFormat";
				args[i++] = dataset.getFormat();
			}
		}
		
		for (Map.Entry<String, ?> param : params.entrySet()) {
			args[i] = "-" + param.getKey();
			args[i+1] = param.getValue().toString();
			i += 2;
		}
		
		return Arrays.copyOf(args, i);
	}
	
	private static final Logger LOGGER = LoggerFactory.getLogger(ParameterizedAlgorithmExecutor.class);

}
