package es.upv.mbda.tfm.zygarde;

import java.util.HashSet;
import java.util.List;
import java.util.Random;
import java.util.Set;
import java.util.stream.Collectors;

import es.upv.mbda.tfm.zygarde.schema.Method;

public class RandomSearchMethodExecutor extends GridSearchMethodExecutor {
	
	private int maxConcurrency;
	
	public RandomSearchMethodExecutor(Method method, JobLifecycle lifecycle, int maxConcurrency) {
		super(method, lifecycle);
		this.maxConcurrency = maxConcurrency;
	}
	
	@Override
	protected List<ParameterizedAlgorithmExecutor> computeTasks(Method method) {
		List<ParameterizedAlgorithmExecutor> tasks = super.computeTasks(method);
		
		Set<Integer> taskIndexes = new HashSet<>(Math.max(this.maxConcurrency, tasks.size()));
		int concurrencyDegree = Math.min(this.maxConcurrency, tasks.size());
		
		Random rand = new Random();
		while (taskIndexes.size() < concurrencyDegree) {
			taskIndexes.add(rand.nextInt(tasks.size()));
		}
		
		return taskIndexes.stream().map(i -> tasks.get(i)).collect(Collectors.toList());
	}
}