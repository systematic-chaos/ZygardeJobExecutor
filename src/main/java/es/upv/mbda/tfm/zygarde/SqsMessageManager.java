package es.upv.mbda.tfm.zygarde;

import java.util.List;
import java.util.stream.Collectors;

import org.json.JSONObject;

import software.amazon.awssdk.services.sqs.SqsClient;
import software.amazon.awssdk.services.sqs.model.DeleteMessageRequest;
import software.amazon.awssdk.services.sqs.model.DeleteMessageResponse;
import software.amazon.awssdk.services.sqs.model.GetQueueUrlRequest;
import software.amazon.awssdk.services.sqs.model.GetQueueUrlResponse;
import software.amazon.awssdk.services.sqs.model.Message;
import software.amazon.awssdk.services.sqs.model.ReceiveMessageRequest;
import software.amazon.awssdk.services.sqs.model.SendMessageRequest;
import software.amazon.awssdk.services.sqs.model.SendMessageResponse;

/**
 * @author thanatos
 * @class es.upv.mbda.tfm.zygarde.SqsMessageManager
 */
public class SqsMessageManager {
	
	private String queueName;
	private String queueUrl;
	private SqsClient sqsClient;
	
	public SqsMessageManager(String queueName) {
		this.queueName = queueName;
		this.sqsClient = SqsClient.create();
		this.queueUrl = getQueueUrl();
	}
	
	public SqsMessageManager(String queueName, String queueUrl) {
		this.queueName = queueName;
		this.queueUrl = queueUrl;
		this.sqsClient = SqsClient.create();
	}
	
	public SqsMessageManager(String queueName, SqsClient sqsClient) {
		this.queueName = queueName;
		this.sqsClient = sqsClient;
		this.queueUrl = getQueueUrl();
	}
	
	public SqsMessageManager(String queueName, String queueUrl, SqsClient sqsClient) {
		this.queueName = queueName;
		this.queueUrl = queueUrl;
		this.sqsClient = sqsClient;
	}
	
	public String getQueueName() {
		return queueName;
	}
	
	public void setQueueName(String queueName) {
		this.queueName = queueName;
		this.queueUrl = getQueueUrl();
	}
	
	public String getQueueUrl() {
		return queueUrl == null ? requestQueueUrl().queueUrl() : queueUrl;
	}
	
	public SqsClient getSqsClient() {
		return sqsClient;
	}
	
	private GetQueueUrlResponse requestQueueUrl() {
		return sqsClient.getQueueUrl(GetQueueUrlRequest.builder().queueName(queueName).build());
	}
	
	public List<Message> receiveMessages() {
		return receiveMessages(1, 20, false);
	}
	
	public List<Message> receiveMessages(Integer maxNumberOfMessages, Integer waitTimeSeconds, boolean deleteOnReceive) {
		List<Message> messages = sqsClient.receiveMessage(ReceiveMessageRequest.builder()
				.queueUrl(queueUrl)
				.maxNumberOfMessages(maxNumberOfMessages)
				.waitTimeSeconds(waitTimeSeconds)
				.build()).messages();
		if (deleteOnReceive) {
			deleteMessages(messages);
		}
		return messages;
	}
	
	public SendMessageResponse sendMessage(String message) {
		return sqsClient.sendMessage(SendMessageRequest.builder()
				.queueUrl(queueUrl)
				.messageBody(message)
				.build());
	}
	
	public List<SendMessageResponse> sendMessage(List<String> messages) {
		return messages.stream().map(msg -> sendMessage(msg)).collect(Collectors.toList());
	}
	
	public SendMessageResponse sendJsonMessage(JSONObject message) {
		return sendMessage(message.toString());
	}
	
	public List<SendMessageResponse> sendJsonMessage(List<JSONObject> messages) {
		return messages.stream().map(msg -> sendMessage(msg.toString())).collect(Collectors.toList());
	}
	
	public DeleteMessageResponse deleteMessage(Message message) {
		return sqsClient.deleteMessage(DeleteMessageRequest.builder()
				.queueUrl(queueUrl)
				.receiptHandle(message.receiptHandle())
				.build());
	}
	
	public List<DeleteMessageResponse> deleteMessages(List<Message> messages) {
		return messages.stream().map(msg -> deleteMessage(msg)).collect(Collectors.toList());
	}
}
