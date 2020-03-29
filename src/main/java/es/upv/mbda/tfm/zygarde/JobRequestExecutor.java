package es.upv.mbda.tfm.zygarde;

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
import es.upv.mbda.tfm.zygarde.schema.ZygardeRequest;

/**
 * @author thanatos
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
		
		List<MethodExecutor> tasks = request.getMethods().stream()
				.map(method -> new BayesianOptimizationMethodExecutor(method, lifecycle))
				.collect(Collectors.toList());
		/*List<MethodExecutor> tasks = request.getMethods().stream()
				.map(method -> new GridSearchMethodExecutor(method, lifecycle))
				.collect(Collectors.toList());*/
		/*List<MethodExecutor> tasks = request.getMethods().stream()
				.map(method -> new RandomSearchMethodExecutor(method, lifecycle,
						request.getComputationalResources().getMaxTotalInstances()))
				.collect(Collectors.toList());*/
		
		ExecutorService executor = Executors.newFixedThreadPool(tasks.size());
		try {
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
	
	private static final Logger LOGGER = LoggerFactory.getLogger(JobRequestExecutor.class);
}
