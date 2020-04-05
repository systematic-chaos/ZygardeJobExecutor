package es.upv.mbda.tfm.zygarde;

import java.io.IOException;
import java.io.InputStream;
import java.net.URISyntaxException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Collection;
import java.util.UUID;

import org.json.JSONException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import es.upv.mbda.tfm.zygarde.result.ModelResult;
import es.upv.mbda.tfm.zygarde.result.Result;
import es.upv.mbda.tfm.zygarde.schema.ZygardeRequest;

/**
 * @author thanatos
 * @class es.upv.mbda.tfm.zygarde.FileSystemResourcesEntryPoint
 */
public class FileSystemResourcesEntryPoint {
	
	private static final String JSON_SCHEMA = "request/json-schema.json";
	// private static final String[] JSON_REQUESTS = { "request/request-body.json", "request/request-body-full.json" };
	private static final String[] JSON_REQUESTS = { "request/request-smac.json" };
	
	private static final Logger LOGGER = LoggerFactory.getLogger(FileSystemResourcesEntryPoint.class);
	
	public static void main(String[] args) {
		InputStream schemaStream = FileSystemResourcesEntryPoint.class
				.getClassLoader().getResourceAsStream(JSON_SCHEMA);
		RequestParser requestParser = new RequestParser(schemaStream);
		Collection<Thread> jobExecutorThreads = new ArrayList<>(JSON_REQUESTS.length);
		
		for (String jsonRequestFile : JSON_REQUESTS) {
			String messageId = UUID.randomUUID().toString();
			LOGGER.info(String.format("Request %s\tProcessing file %s", messageId, jsonRequestFile));
			try {
				String jsonRequest = new String(Files.readAllBytes(
						Paths.get(FileSystemResourcesEntryPoint.class.getClassLoader()
								.getResource(jsonRequestFile).toURI())),
						StandardCharsets.UTF_8);
				if (requestParser.validateSchema(jsonRequest)) {
					ZygardeRequest request = requestParser.readJson(jsonRequest);
					request.setRequestId(messageId);
					jobExecutorThreads.add(executeJob(request));
				} else {
					LOGGER.warn(String.format("File %s did not match request schema.", jsonRequestFile));
				}
			} catch (JSONException jsone) {
				LOGGER.error("Exception parsing JSON request\n" + jsone.getMessage(), jsone);
			} catch (URISyntaxException | IOException e) {
				LOGGER.error("Exception reading resource file\n" + e.getMessage(), e);
			}
		}
		
		for (Thread t : jobExecutorThreads) {
			try {
				t.join();
			} catch (InterruptedException ie) {
				LOGGER.warn(String.format("InterruptedException when joining thread %s\n%s",
						t.getName(), ie.getMessage()), ie);
			}
		}
	}
	
	private static Thread executeJob(ZygardeRequest requestBody) {
		Thread jobThread = new Thread(new JobRequestExecutor(requestBody,
				new LocalJobLifecycleFinish(requestBody)),
				requestBody.getRequestId());
		jobThread.start();
		return jobThread;
	}
	
	private static class LocalJobLifecycleFinish extends JobLifecycleFinish {
		
		public LocalJobLifecycleFinish(ZygardeRequest request) {
			this.request = request;
		}
		
		public void onFinishTask(ModelResult taskResult) {
			LOGGER.info(taskResult.toString());
		}
		
		public void onFinishExecution(Result finalResult) {
			LOGGER.info(composeExecutionReport(finalResult));
			LOGGER.info(String.format(
					"Finished execution of job from message %s", request.getRequestId()));
		}
	}
}
