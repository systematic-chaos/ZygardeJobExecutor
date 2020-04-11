package es.upv.mbda.tfm.zygarde;

import java.net.URL;
import java.nio.file.Path;
import java.time.Duration;

import software.amazon.awssdk.core.sync.RequestBody;
import software.amazon.awssdk.services.s3.S3Client;
import software.amazon.awssdk.services.s3.model.GetObjectRequest;
import software.amazon.awssdk.services.s3.model.GetUrlRequest;
import software.amazon.awssdk.services.s3.model.PutObjectRequest;
import software.amazon.awssdk.services.s3.model.PutObjectResponse;
import software.amazon.awssdk.services.s3.presigner.S3Presigner;
import software.amazon.awssdk.services.s3.presigner.model.GetObjectPresignRequest;
import software.amazon.awssdk.services.s3.presigner.model.PresignedGetObjectRequest;

/**
 * Zygarde: Platform for reactive training of models in the cloud
 * Master in Big Data Analytics
 * Polytechnic University of Valencia
 * 
 * @author		Javier Fernández-Bravo Peñuela
 * @copyright	2020 Ka-tet Corporation. All rights reserved
 * @license		GPLv3.0
 * @contact		fjfernandezbravo@iti.es
 * 
 * @class es.upv.mbda.tfm.zygarde.S3ObjectManager
 */
public class S3ObjectManager {
	
	private String bucket;
	private S3Client s3Client;
	
	public S3ObjectManager(String bucketName) {
		this(bucketName, S3Client.create());
	}
	
	public S3ObjectManager(String bucket, S3Client s3Client) {
		this.bucket = bucket;
		this.s3Client = s3Client;
	}
	
	public String getBucket() {
		return bucket;
	}
	
	public void setBucket(String bucket) {
		this.bucket = bucket;
	}
	
	public S3Client getS3Client() {
		return s3Client;
	}
	
	public PutObjectResponse uploadFile(String key, Path filePath) {
		return uploadFile(this.bucket, key, this.s3Client, filePath);
	}
	
	public PutObjectResponse uploadFile(String key, RequestBody requestBody) {
		return uploadFile(this.bucket, key, this.s3Client, requestBody);
	}
	
	public PresignedGetObjectRequest presign(String key) {
		return presign(this.bucket, key, S3Presigner.create());
	}
	
	public String getPresignedUrl(String key) {
		return getPresignedUrl(this.bucket, key, S3Presigner.create());
	}
	
	public String getResourceUrl(String key) {
		return getResourceUrl(this.bucket, key, this.s3Client).toExternalForm();
	}
	
	public URL uploadPresignFile(String key, Path filePath) {
		return uploadPresignFile(this.bucket, key, this.s3Client, 
				S3Presigner.create(), filePath);
	}
	
	public URL uploadPresignFile(String key, RequestBody requestBody) {
		return uploadPresignFile(this.bucket, key, this.s3Client,
				S3Presigner.create(), requestBody);
	}
	
	public static PutObjectResponse uploadFile(String bucket, String key, S3Client s3Client,
			Path filePath) {
		return uploadFile(bucket, key, s3Client, RequestBody.fromFile(filePath));
	}
	
	public static PutObjectResponse uploadFile(String bucket, String key, S3Client s3Client,
			RequestBody requestBody) {
		return s3Client.putObject(
				PutObjectRequest.builder().bucket(bucket).key(key).build(),
				requestBody);
	}
	
	public static PresignedGetObjectRequest presign(String bucket, String key, S3Presigner presigner) {
		return presigner.presignGetObject(
				GetObjectPresignRequest.builder()
				.signatureDuration(Duration.ofSeconds(9000))
				.getObjectRequest(GetObjectRequest.builder()
						.bucket(bucket).key(key).build())
				.build());
	}
	
	public static String getPresignedUrl(String bucket, String key, S3Presigner presigner) {
		return presign(bucket, key, presigner).url().toExternalForm();
	}
	
	public static URL getResourceUrl(String bucket, String key, S3Client s3Client) {
		return s3Client.utilities().getUrl(
				GetUrlRequest.builder().bucket(bucket).key(key).build());
	}
	
	public static URL uploadPresignFile(String bucket, String key, S3Client s3Client,
			S3Presigner presigner, Path filePath) {
		uploadFile(bucket, key, s3Client, filePath);
		return presign(bucket, key, presigner).url();
	}
	
	public static URL uploadPresignFile(String bucket, String key, S3Client s3Client,
			S3Presigner presigner, RequestBody requestBody) {
		uploadFile(bucket, key, s3Client, requestBody);
		return presign(bucket, key, presigner).url();
	}
}
