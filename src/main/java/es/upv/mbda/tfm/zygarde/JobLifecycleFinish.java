package es.upv.mbda.tfm.zygarde;

import java.text.DecimalFormat;
import java.text.DecimalFormatSymbols;

import es.upv.mbda.tfm.zygarde.result.ModelResult;
import es.upv.mbda.tfm.zygarde.result.Result;
import es.upv.mbda.tfm.zygarde.schema.ZygardeRequest;

/**
 * @author thanatos
 * @class es.upv.mbda.tfm.zygarde.JobLifecycleFinish
 */
public abstract class JobLifecycleFinish implements JobLifecycle {
	
	protected ZygardeRequest request;
	
	protected static DecimalFormat precisionFormatter;
	static {
		DecimalFormatSymbols decimalSeparator = DecimalFormatSymbols.getInstance();
		decimalSeparator.setDecimalSeparator(',');
		precisionFormatter = new DecimalFormat("0.000#", decimalSeparator);
	}
	
	protected String composeExecutionReport(Result executionResult) {
		StringBuilder executionReport = new StringBuilder(
				String.format(
						"Best precision: %1.4f\tAlgorithm: %s\n\n",
						executionResult.getBestPrecision(),
						executionResult.getBestResult().getAlgorithm()));
		
		for (ModelResult result : executionResult.getResults()) {
			executionReport.append(result.toString()).append('\n');
		}
		
		return executionReport.toString();
	}
}
