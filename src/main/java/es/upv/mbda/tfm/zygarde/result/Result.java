package es.upv.mbda.tfm.zygarde.result;

import java.util.ArrayList;
import java.util.Collection;
import java.util.Comparator;
import java.util.List;
import java.util.SortedSet;
import java.util.TreeSet;

public class Result {
	
	protected SortedSet<ModelResult> results;
	
	public Result() {
		results = new TreeSet<>(Comparator.reverseOrder());
	}
	
	public Result(Collection<ModelResult> results) {
		this();
		this.setResults(results);
	}
	
	public SortedSet<ModelResult> getResults() {
		return this.results;
	}
	
	public void setResults(Collection<ModelResult> results) {
		this.results.clear();
		this.addResults(results);
	}
	
	public List<ModelResult> getResultsList() {
		return new ArrayList<>(this.results);
	}
	
	public void addResult(ModelResult r) {
		this.results.add(r);
	}
	
	public void addResults(Collection<ModelResult> r) {
		this.results.addAll(r);
	}
	
	public ModelResult getBestResult() {
		return !results.isEmpty() ? results.first() : null;
	}
	
	public Double getBestPrecision() {
		return !results.isEmpty() ? results.first().getPrecision() : 0.;
	}
}
