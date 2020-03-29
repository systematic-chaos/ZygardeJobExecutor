package es.upv.mbda.tfm.zygarde;

import es.upv.mbda.tfm.zygarde.result.ModelResult;
import es.upv.mbda.tfm.zygarde.result.Result;

/**
 * @author thanatos
 * @class es.upv.mbda.tfm.zygarde.JobLifecycle
 */
public interface JobLifecycle {
	
	void onFinishExecution(Result finalResult);
	
	void onFinishTask(ModelResult taskResult);
}
