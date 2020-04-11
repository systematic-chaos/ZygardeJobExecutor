package es.upv.mbda.tfm.zygarde;

import java.io.IOException;
import java.io.InputStream;
import java.util.List;

import org.json.JSONException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import es.upv.mbda.tfm.zygarde.result.ModelResult;
import es.upv.mbda.tfm.zygarde.result.Result;
import es.upv.mbda.tfm.zygarde.schema.ZygardeRequest;
import software.amazon.awssdk.core.sync.RequestBody;
import software.amazon.awssdk.services.sqs.model.Message;

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
 * @class es.upv.mbda.tfm.zygarde.SqsEntryPoint
 */
public class SqsEntryPoint {
	
	private static final String QUEUE_NAME = "ZygardeQueue";
	private static final Logger LOGGER = LoggerFactory.getLogger(SqsEntryPoint.class);
	
	private static SqsMessageManager sqs = new SqsMessageManager(QUEUE_NAME);
	private static S3ObjectManager s3 = new S3ObjectManager(AwsJobLifecycleFinish.MODEL_BUCKET);
	
	public static void main(String[] args) {
		String queueUrl = sqs.getQueueUrl();
		
		LOGGER.info("Queue: " + QUEUE_NAME);
		LOGGER.info("Queue URL: " + queueUrl);
		
		InputStream schemaStream = SqsMessageManager.class.getClassLoader().getResourceAsStream("request/json-schema.json");
		RequestParser requestParser = new RequestParser(schemaStream);
		
		while (true) {
			List<Message> messages = sqs.receiveMessages();
			if (!messages.isEmpty()) {
				for (Message msg : messages) {
					LOGGER.info(String.format("Received message %s", msg.messageId()));
					try {
						if (requestParser.validateSchema(msg.body())) {
								ZygardeRequest requestBody = requestParser.readJson(msg.body());
								requestBody.setRequestId(msg.messageId());
								executeJob(msg, requestBody);
						} else {
							LOGGER.warn(String.format("Message %s did not match request schema.", msg.messageId()));
						}
					} catch (JSONException | IOException e) {
						LOGGER.error("Exception parsing JSON request\n" + e.getMessage(), e);
					}
				}
			} else {
				try {
					Thread.sleep(50000);
				} catch (InterruptedException ie) {
					LOGGER.warn("InterruptedException: " + ie.getMessage());
				}
			}
		}
	}
	
	private static Thread executeJob(Message requestMessage, ZygardeRequest requestBody) {
		Thread jobThread = new Thread(new JobRequestExecutor(requestBody,
				new AwsJobLifecycleFinish(requestBody, requestMessage)),
				requestBody.getRequestId());
		jobThread.start();
		return jobThread;
	}
	
	private static class AwsJobLifecycleFinish extends JobLifecycleFinish {
		static final String MODEL_BUCKET = "zygarde-model";
		static final String RESULT_BUCKET = "zygarde-result";
		
		private Message requestMessage;
		
		public AwsJobLifecycleFinish(ZygardeRequest request, Message requestMessage) {
			this.request = request;
			this.requestMessage = requestMessage;
		}
		
		public void onFinishTask(ModelResult taskResult) {
			String taskResultMessage = taskResult.toString();
			String s3Key = composePath(taskResult).toString();
			String reportS3Key = composeReportPath(taskResult);
			String modelS3Key  = composeModelPath(taskResult);
			
			s3.uploadFile(reportS3Key, RequestBody.fromString(taskResultMessage));
			s3.uploadFile(modelS3Key, RequestBody.fromString(s3Key));
			
			LOGGER.info(taskResultMessage);
			LOGGER.info(String.format("Uploaded %s to %s AWS S3 bucket", reportS3Key, MODEL_BUCKET));
			LOGGER.info(String.format("Uploaded %s to %s AWS S3 bucket", modelS3Key,  MODEL_BUCKET));
		}
		
		public void onFinishExecution(Result finalResult) {
			String fileKey = String.format("%s/%s.txt",
					request.getEmailAddress(), request.getRequestId());
			
			S3ObjectManager.uploadFile(RESULT_BUCKET,
					fileKey,
					s3.getS3Client(),
					RequestBody.fromString(composeExecutionReport(finalResult)));
			
			sqs.deleteMessage(requestMessage);
			
			LOGGER.info(String.format(
					"Uploaded %s to %s S3 bucket",
					fileKey, RESULT_BUCKET));
			LOGGER.info(String.format(
					"Finished execution of job from message %s", request.getRequestId()));
		}
		
		@Override
		protected String composeExecutionReport(Result executionResult) {
			StringBuilder executionReport = new StringBuilder(
					String.format(
							"Best precision: %1.4f\tAlgorithm: %s\t%s\n\n",
							executionResult.getBestPrecision(),
							executionResult.getBestResult().getAlgorithm(),
							s3.getPresignedUrl(composeModelPath(executionResult.getBestResult()))));
			
			for (ModelResult result : executionResult.getResults()) {
				String resultModelUrl = s3.getResourceUrl(composeModelPath(result));
				executionReport.append(result.toString())
						.append('\t').append(resultModelUrl).append('\n');
			}
			
			return executionReport.toString();
		}
		
		private StringBuilder composePath(ModelResult taskResult) {
			return new StringBuilder(request.getRequestId())
					.append('/').append(request.getDomain())
					.append('/').append(precisionFormatter.format(taskResult.getPrecision()))
					.append('-').append(taskResult.getAlgorithm());
		}
		
		private String composeReportPath(ModelResult taskResult) {
			return composePath(taskResult).append('-').append("report").append(".txt").toString();
		}
		
		private String composeModelPath(ModelResult taskResult) {
			return composePath(taskResult).append('-').append("model").append(".txt").toString();
		}
	}
}
