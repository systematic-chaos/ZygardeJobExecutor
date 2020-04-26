package es.upv.mbda.tfm.zygarde;

import java.io.File;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.io.IOException;
import java.net.URL;
import java.nio.channels.Channels;
import java.nio.channels.FileChannel;
import java.nio.channels.ReadableByteChannel;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.SortedSet;
import java.util.TreeSet;
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
import es.upv.mbda.tfm.zygarde.result.Result;
import es.upv.mbda.tfm.zygarde.schema.ParameterSearch;
import es.upv.mbda.tfm.zygarde.schema.ZygardeRequest;

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
 * @class es.upv.mbda.tfm.zygarde.JobRequestExecutor
 */
public class JobRequestExecutor implements Runnable {
	
	private ZygardeRequest request;
	private JobLifecycle lifecycle;
	
	public JobRequestExecutor(ZygardeRequest request, JobLifecycle lifecycle) {
		this.request = request;
		this.lifecycle = lifecycle;
	}
	
	@Override
	public void run() {
		Result result = executeRequest();
		lifecycle.onFinishExecution(result);
	}
	
	public Result executeRequest() {
		LOGGER.info(request.toString());
		
		SortedSet<ModelResult> globalResults = new TreeSet<>(Comparator.reverseOrder());
		List<MethodExecutor> tasks = prepareTasks();
		
		try {
			transferDatasetToS3();
			
			ExecutorService executor = Executors.newFixedThreadPool(tasks.size());
			List<Future<AlgorithmResult>> taskResults = executor.invokeAll(tasks);
			executor.shutdown();
			if (!executor.awaitTermination(12l, TimeUnit.HOURS)) {
				executor.shutdownNow();
			}
			
			for (Future<AlgorithmResult> partialResult : taskResults) {
				globalResults.addAll(partialResult.get().getResults());
			}
			LOGGER.info(String.format("Best precision: %1.4f\tAlgorithm: %s",
					globalResults.first().getPrecision(),
					globalResults.first().getAlgorithm()));
		} catch (IOException ioe) {
			LOGGER.error("IOException while transferring dataset to AWS S3: " + ioe.getMessage());
		} catch (InterruptedException | ExecutionException e) {
			LOGGER.error("Interrupted exception on request's methods execution\n"
					+ e.getMessage(), e);
		}
		
		return new Result(new ArrayList<>(globalResults));
	}
	
	public Result executeRequest(ZygardeRequest request) {
		this.request = request;
		return executeRequest();
	}
	
	private List<MethodExecutor> prepareTasks() {
		List<MethodExecutor> tasks;
		switch (ParameterSearch.forName(request.getParameterSearch())) {
		case BAYESIAN_OPTIMIZATION:
			tasks = request.getMethods().stream()
				.map(method -> new BayesianOptimizationMethodExecutor(request.getRequestId(), method, request.getDataset(), lifecycle))
				.collect(Collectors.toList());
			break;
		case GRID:
			tasks = request.getMethods().stream()
				.map(method -> new GridSearchMethodExecutor(request.getRequestId(), method, request.getDataset(), lifecycle))
				.collect(Collectors.toList());
			break;
		case RANDOM:
			int concurrencyDegree = request.getComputationalResources() != null
				&& request.getComputationalResources().getMaxTotalInstances() != null ?
						request.getComputationalResources().getMaxTotalInstances()
						: Runtime.getRuntime().availableProcessors();
			tasks = request.getMethods().stream()
				.map(method -> new RandomSearchMethodExecutor(request.getRequestId(), method, request.getDataset(), lifecycle, concurrencyDegree))
				.collect(Collectors.toList());
			break;
		default:
			tasks = new ArrayList<>(0);
		}
		return tasks;
	}
	
	private void transferDatasetToS3() throws IOException {
		// The dataset is already available from AWS S3
		if (request.getDataset() == null || request.getDataset().getPath().startsWith("s3")) {
			return;
		}
		
		String requestDatasetPath = request.getDataset().getPath();
		
		// Local filesystem dataset. Useful for local development and debugging.
		File requestDatasetFile = new File(requestDatasetPath);
		if (requestDatasetFile.exists() && requestDatasetFile.isFile()) {
			return;
		}
		
		File datasetDir = Paths.get("/tmp", request.getRequestId()).toFile();
		File datasetFile = Paths.get(datasetDir.getPath(),
				requestDatasetPath.substring(requestDatasetPath.lastIndexOf(File.separator) + 1)).toFile();
		
		datasetDir.mkdir();
		
		try (InputStream is = new URL(request.getDataset().getPath()).openStream();
				FileOutputStream fos = new FileOutputStream(datasetFile)) {
			ReadableByteChannel rbc = Channels.newChannel(is);
			FileChannel fc = fos.getChannel();
			fc.transferFrom(rbc, 0, Long.MAX_VALUE);
		}
		
		S3ObjectManager s3Client = new S3ObjectManager("zygarde-data");
		s3Client.uploadFile(
				String.join(File.separator, datasetDir.getName(), datasetFile.getName()),
				datasetFile.toPath());
		
		request.getDataset().setPath(String.join(File.separator, "s3a:/",
				s3Client.getBucket(), datasetDir.getName(), datasetFile.getName()));
		
		datasetFile.delete();
		datasetDir.delete();
	}
	
	private static final Logger LOGGER = LoggerFactory.getLogger(JobRequestExecutor.class);
}
