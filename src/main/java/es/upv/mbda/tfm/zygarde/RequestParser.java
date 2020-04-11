package es.upv.mbda.tfm.zygarde;

import java.io.IOException;
import java.io.InputStream;

import org.everit.json.schema.Schema;
import org.everit.json.schema.ValidationException;
import org.everit.json.schema.loader.SchemaLoader;
import org.json.JSONException;
import org.json.JSONObject;
import org.json.JSONTokener;

import com.fasterxml.jackson.databind.DeserializationFeature;
import com.fasterxml.jackson.databind.ObjectMapper;

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
 * @class es.upv.mbda.tfm.zygarde.RequestParser
 */
public class RequestParser {
	
	private Schema schema;
	private ObjectMapper objectMapper;
	
	public RequestParser(String jsonSchema) {
		this(new JSONObject(new JSONTokener(jsonSchema)));
	}
	
	public RequestParser(InputStream jsonSchema) {
		this(new JSONObject(new JSONTokener(jsonSchema)));
	}
	
	public RequestParser(JSONObject jsonSchema) {
		schema = SchemaLoader.load(jsonSchema);
		
		objectMapper = new ObjectMapper();
		objectMapper.configure(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES, false);
		objectMapper.configure(DeserializationFeature.FAIL_ON_NULL_FOR_PRIMITIVES, true);
		objectMapper.configure(DeserializationFeature.USE_JAVA_ARRAY_FOR_JSON_ARRAY, false);
	}
	
	public boolean validateSchema(String jsonDocument) throws JSONException {
		return validateSchema(new JSONObject(jsonDocument));
	}
	
	public boolean validateSchema(String jsonSchema, String jsonDocument) throws JSONException {
		return validateSchema(new JSONObject(jsonSchema), new JSONObject(jsonDocument));
	}
	
	public boolean validateSchema(JSONObject jsonDocument) throws JSONException {
		return validateSchema(this.schema, jsonDocument);
	}
	
	public boolean validateSchema(JSONObject jsonSchema, JSONObject jsonDocument)
			throws JSONException {
		return validateSchema(SchemaLoader.load(jsonSchema), jsonDocument);
	}
	
	public static boolean validateSchema(Schema jsonSchema, JSONObject jsonDocument)
			throws JSONException {
		try {
			jsonSchema.validate(jsonDocument);
		} catch (ValidationException ve) {
			return false;
		}
		return true;
	}
	
	public ZygardeRequest readJson(String jsonString) throws IOException {
		return objectMapper.readValue(jsonString, ZygardeRequest.class);
	}
	
	public ZygardeRequest readJson(InputStream jsonStream) throws IOException {
		return objectMapper.readValue(jsonStream, ZygardeRequest.class);
	}
}
