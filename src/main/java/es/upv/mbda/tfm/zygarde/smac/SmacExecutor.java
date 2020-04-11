package es.upv.mbda.tfm.zygarde.smac;

import java.io.File;
import java.io.IOException;
import java.io.PrintWriter;
import java.io.StringWriter;
import java.lang.management.ManagementFactory;
import java.net.InetAddress;
import java.net.UnknownHostException;
import java.text.DecimalFormat;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Map;
import java.util.SortedMap;
import java.util.TreeMap;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.slf4j.Marker;
import org.slf4j.MarkerFactory;

import com.beust.jcommander.JCommander;
import com.beust.jcommander.ParameterException;

import ca.ubc.cs.beta.aeatk.algorithmexecutionconfiguration.AlgorithmExecutionConfiguration;
import ca.ubc.cs.beta.aeatk.algorithmrunresult.AlgorithmRunResult;
import ca.ubc.cs.beta.aeatk.exceptions.StateSerializationException;
import ca.ubc.cs.beta.aeatk.exceptions.TrajectoryDivergenceException;
import ca.ubc.cs.beta.aeatk.logging.CommonMarkers;
import ca.ubc.cs.beta.aeatk.misc.jcommander.JCommanderHelper;
import ca.ubc.cs.beta.aeatk.misc.returnvalues.AEATKReturnValues;
import ca.ubc.cs.beta.aeatk.misc.spi.SPIClassLoaderHelper;
import ca.ubc.cs.beta.aeatk.misc.version.JavaVersionInfo;
import ca.ubc.cs.beta.aeatk.misc.version.OSVersionInfo;
import ca.ubc.cs.beta.aeatk.misc.version.VersionTracker;
import ca.ubc.cs.beta.aeatk.misc.watch.AutoStartStopWatch;
import ca.ubc.cs.beta.aeatk.misc.watch.StopWatch;
import ca.ubc.cs.beta.aeatk.options.AbstractOptions;
import ca.ubc.cs.beta.aeatk.parameterconfigurationspace.ParameterConfiguration;
import ca.ubc.cs.beta.aeatk.probleminstance.InstanceListWithSeeds;
import ca.ubc.cs.beta.aeatk.probleminstance.ProblemInstanceOptions.TrainTestInstances;
import ca.ubc.cs.beta.aeatk.probleminstance.ProblemInstanceSeedPair;
import ca.ubc.cs.beta.aeatk.random.SeedableRandomPool;
import ca.ubc.cs.beta.aeatk.runhistory.RunHistory;
import ca.ubc.cs.beta.aeatk.smac.SMACOptions;
import ca.ubc.cs.beta.aeatk.state.StateFactoryOptions;
import ca.ubc.cs.beta.aeatk.targetalgorithmevaluator.exceptions.TargetAlgorithmAbortException;
import ca.ubc.cs.beta.aeatk.termination.TerminationCondition;
import ca.ubc.cs.beta.aeatk.trajectoryfile.TrajectoryFileEntry;
import ca.ubc.cs.beta.smac.builder.SMACBuilder;
import ca.ubc.cs.beta.smac.configurator.AbstractAlgorithmFramework;
import ca.ubc.cs.beta.smac.misc.version.SMACVersionInfo;
import ca.ubc.cs.beta.smac.validation.ValidationResult;

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
 * @class es.upv.mbda.tfm.zygarde.smac.SmacExecutor
 */
public class SmacExecutor {
	
	private Map<String, AbstractOptions> taeOptions;
	private String runGroupName = "DEFAULT";
	private String outputDir;
	private String logLocation;
	private SeedableRandomPool pool;
	private InstanceListWithSeeds trainingILWS;
	
	private static final Logger LOGGER = LoggerFactory.getLogger(SmacExecutor.class);
	private static final Marker EXCEPTION = MarkerFactory.getMarker("EXCEPTION");
	private static final Marker STACK_TRACE = MarkerFactory.getMarker("STACKTRACE");
	private static final String PROGRAM_NAME = "ZygardeSmac";
	
	static {
		VersionTracker.setClassLoader(SPIClassLoaderHelper.getClassLoader());
		
		VersionTracker.logVersions();
		SMACVersionInfo s = new SMACVersionInfo();
		JavaVersionInfo j = new JavaVersionInfo();
		OSVersionInfo o = new OSVersionInfo();
		LOGGER.info(CommonMarkers.SKIP_FILE_PRINTING, "Version of {} is {}, running on {} and {}",
				s.getProductName(), s.getVersion(), j.getVersion(), o.getVersion());
	}
	
	public List<AlgorithmRunResult> runSmac(String[] args) {
		List<AlgorithmRunResult> result = new ArrayList<>();
		if (runSmac(args, result) != AEATKReturnValues.SUCCESS) {
			result.clear();
		}
		return result;
	}
	
	public int runSmac(String[] args, List<AlgorithmRunResult> result) {
		try {
			SMACOptions options = parseCliOptions(args);
			
			SMACBuilder smacBuilder = new SMACBuilder();
			
			AlgorithmExecutionConfiguration execConfig = options.getAlgorithmExecutionConfig();
			
			AbstractAlgorithmFramework smac = smacBuilder.getAutomaticConfigurator(
					execConfig, this.trainingILWS, options, this.taeOptions, this.outputDir, this.pool);
			
			StopWatch watch = new AutoStartStopWatch();
			
			smac.run();
			
			watch.stop();
			
			smacBuilder.getLogRuntimeStatistics().logLastRuntimeStatistics();
			
			pool.logUsage();
			
			logSmacTermination(smac);
			
			List<TrajectoryFileEntry> tfes = smacBuilder.getTrajectoryFileLogger().getTrajectoryFileEntries();
			SortedMap<TrajectoryFileEntry, ValidationResult> performance = new TreeMap<>();
			performance.put(tfes.get(tfes.size() - 1),
					new ValidationResult(Double.POSITIVE_INFINITY, Collections.<ProblemInstanceSeedPair>emptyList()));
			
			result.addAll(smac.runHistory().getAlgorithmRunsExcludingRedundant(/*smac.getIncumbent()*/));
			
			smacBuilder.getEventManager().shutdown();
			
			LOGGER.info(new StringBuilder("\n------------------------------------------------------------\n")
					.append(String.format("Additional information about run %d in: %s\n", options.seedOptions.numRun, this.outputDir))
					.append("------------------------------------------------------------").toString());
		} catch(ParameterException pe) {
			LOGGER.error("Error occurred while running SMAC\n>Error Message: " + pe.getMessage());
			LOGGER.info("Note that some options are read from files in ~/.aeatk/");
			LOGGER.debug("Exception stack trace", pe);
			return AEATKReturnValues.PARAMETER_EXCEPTION;
		} catch (TargetAlgorithmAbortException taae) {
			LOGGER.error("Error occurred while running SMAC\n>Error Message: " + taae.getMessage());
			LOGGER.error(new StringBuilder().append("We tried to call the target algorithm wrapper, but this call failed.\n")
				.append("The problem is (most likely) somewhere in the wrapper or with the arguments to SMAC.\n")
				.append("The easiest way to debug this problem is to manually execute the call we tried and see why it did not return the correct result.\n")
				.append("The required output of the wrapper is something like \"Result for ParamILS: x,x,x,x,x\".);\n").toString());
			return AEATKReturnValues.OTHER_EXCEPTION;
		} catch (StateSerializationException sse) {
			LOGGER.error("Error occurred while running SMAC\n>Error Message: " + sse.getMessage());
			return AEATKReturnValues.SERIALIZATION_EXCEPTION;
		} catch (TrajectoryDivergenceException tde) {
			LOGGER.error("Error occurred while running SMAC\n>Error Message: " + tde.getMessage());
			return AEATKReturnValues.TRAJECTORY_DIVERGENCE;
		} catch (Exception e) {
			LOGGER.error("Error occurred while running SMAC\n>Error Message: " + e.getMessage()
					+ "\n>Encountered Exception: " + e.getClass().getSimpleName()
					+ "\n>ErrorLogLocation: " + this.logLocation);
			LOGGER.error("Message: " + e.getMessage(), e);
			
			LOGGER.info("Maybe try running in DEBUG mode if you are missing information");
			LOGGER.error(EXCEPTION, "Exception: {}", e.getClass().getCanonicalName());
			StringWriter sWriter = new StringWriter();
			PrintWriter writer = new PrintWriter(sWriter);
			e.printStackTrace(writer);
			LOGGER.error(STACK_TRACE, "Stack Trace: {}", sWriter.toString());
			
			LOGGER.info(new StringBuilder("Exiting SMAC with failure. Log: " + logLocation + "\n")
					.append("For a list of available commands use: --help\n")
					.append("The Quickstart guide is available t: http://www.cs.ubc.ca/labs/beta/Projects/SMAC/ ")
					.append("or alternatively (doc/quickstart.html) gives simple examples for getting up and running.\n")
					.append("The FAQ (doc/faq.pdf) contains commonly asked questions regarding troubleshooting, and usage.\n")
					.append("The Manual (doc/manual.pdf) contains detailed information on file format semantics.\n")
					.append("If you are stuck, please ask a question in the SMAC forum: https://groups.google.com/forum/#!forum/smac-forum")
					.append('\n').toString());
			
			return AEATKReturnValues.OTHER_EXCEPTION;
		}
		
		return AEATKReturnValues.SUCCESS;
	}
		
	/**
	 * Parses Command Line Arguments and returns an Options object
	 * @param args Command line arguments
	 * @return An options object
	 * @throws ParameterException Something has gone wrong while parsing parameters
	 * @throws IOException An I/O exception of some sort has occurred
	 */
	private SMACOptions parseCliOptions(String[] args) throws ParameterException, IOException {
		SMACOptions options = new SMACOptions();
		this.taeOptions = options.scenarioConfig.algoExecOptions.taeOpts.getAvailableTargetAlgorithmEvaluators();
		JCommander jcom = JCommanderHelper.getJCommanderAndCheckForHelp(args, options, this.taeOptions);
		
		jcom.setProgramName(PROGRAM_NAME);
		
		try {
			args = processScenarioStateRestore(jcom, options, args);
			
			setupAdaptiveCapping(options);
			setupRandomForestOptionsLogModel(options);
			
			this.runGroupName = options.getRunGroupName(this.taeOptions.values());
			
			createOutputDirectory(options);
			
			finalizeCliOptionsParsing(options, jcom);
			
			logSystemHostnameEnvironmentProperties(jcom, args);
			
			this.pool = options.seedOptions.getSeedableRandomPool();
			
			TrainTestInstances tti = options.getTrainingAndTestProblemInstances(this.pool, new SeedableRandomPool(options.validationSeed + options.seedOptions.seedOffset, pool.getInitialSeeds()));
			this.trainingILWS = tti.getTrainingInstances();
			
			logJvmCpuTimeMeasurements(options);
		} catch (IOException | ParameterException e) {
			LOGGER.error("SmacExecutor.parseCliOptions\n" + e.getMessage(), e);
			throw e;
		}
		
		return options;
	}
	
	private String[] processScenarioStateRestore(JCommander jcom, SMACOptions options,
			String[] args) {
		try {
			args = StateFactoryOptions.processScenarioStateRestore(args);
			jcom.parse(args);
		} finally {
			runGroupName = options.runGroupOptions.getFailbackRunGroup();
		}
		return args;
	}
	
	private SMACOptions setupAdaptiveCapping(SMACOptions options) {
		if (options.adaptiveCapping == null) {
			switch(options.scenarioConfig.getRunObjective()) {
			case RUNTIME:
				options.adaptiveCapping = true;
				break;
			
			case QUALITY:
				options.adaptiveCapping = false;
				break;
			
			default:
				throw new IllegalStateException("Not sure what to default too, "
						+ "you may need to add something new here.");
			}
		}
		return options;
	}
	
	private SMACOptions setupRandomForestOptionsLogModel(SMACOptions options) {
		if (options.randomForestOptions.logModel == null) {
			switch (options.scenarioConfig.getRunObjective()) {
			case RUNTIME:
				options.randomForestOptions.logModel = true;
				break;
			case QUALITY:
				options.randomForestOptions.logModel = false;
				break;
			default:
				throw new IllegalStateException("Unsure what to do with new run objective");
			}
		}
		return options;
	}
	
	/**
	 *  Build the Serializer used in the model
	 */
	private void createOutputDirectory(SMACOptions options) {
		this.outputDir = options.getOutputDirectory(this.runGroupName);
		
		File outputDirFile = new File(this.outputDir);
		if (!outputDirFile.exists()) {
			outputDirFile.mkdirs();
			
			// Check again to ensure there isn't a race condition
			if (!outputDirFile.exists()) {
				throw new ParameterException("Could not create all folders necessary for output directory: " + this.outputDir);
			}
		}
	}
	
	private void logSystemHostnameEnvironmentProperties(JCommander jcom, String[] args) {
		JCommanderHelper.logCallString(args, PROGRAM_NAME);
		
		final Map<String, String> env = System.getenv();
		
		StringBuilder sb = new StringBuilder();
		for (String envName : env.keySet()) {
			sb.append(envName).append('=').append(env.get(envName)).append('\n');
		}
		LOGGER.debug(CommonMarkers.SKIP_CONSOLE_PRINTING, "******** The next bit of output can be ignored, it is merely useful for debugging ********");
		LOGGER.debug(CommonMarkers.SKIP_CONSOLE_PRINTING, "======== Environment Variables ========\n{}", sb.toString());
		
		final Map<Object, Object> props = new TreeMap<>(System.getProperties());
		sb = new StringBuilder();
		for (Map.Entry<Object, Object> ent : props.entrySet()) {
			sb.append(ent.getKey().toString()).append('=').append(ent.getValue().toString()).append('\n');
		}
		
		String hostname;
		try {
			hostname = InetAddress.getLocalHost().getHostName();
		} catch (UnknownHostException uhe) {
			// If this fails it's okay, we just use it to output the log
			hostname = "[UNABLE TO DETERMINE HOSTNAME]";
			LOGGER.warn(hostname, uhe);
		}
		
		LOGGER.debug(CommonMarkers.SKIP_CONSOLE_PRINTING, "Hostname: {}", hostname);
		LOGGER.debug(CommonMarkers.SKIP_CONSOLE_PRINTING, "======== System Properties ========\n{}", sb.toString());
		
		JCommanderHelper.logConfigurationInfoToFile(jcom);
	}
	
	private void finalizeCliOptionsParsing(SMACOptions options, JCommander jcom)
			throws IOException, ParameterException {
		options.logOptions.initializeLogging(this.outputDir, options.seedOptions.numRun);
		this.logLocation = options.logOptions.getLogLocation(this.outputDir, options.seedOptions.numRun);
		
		for (String name : jcom.getParameterFilesToRead()) {
			LOGGER.debug("Parsing (default) options from file: {}\n", name);
		}
	}
	
	/**
	 * We don't handle this more gracefully because this seems like a super rare incident.
	 */
	private void logJvmCpuTimeMeasurements(SMACOptions options) {
		try {
			if (ManagementFactory.getThreadMXBean().isThreadCpuTimeEnabled()) {
				LOGGER.trace("JVM Supports CPU Timing Measurements");
			} else {
				LOGGER.warn("Trying to enable CPU Time Measurements on this Java Virtual Machine...");
				ManagementFactory.getThreadMXBean().setThreadCpuTimeEnabled(true);
				LOGGER.warn("CPU Time Measurements were successfully enabled, "
						+ "tunerTimeout will contain SMAC Execution Time Information");
			}
		} catch (UnsupportedOperationException | SecurityException e) {
			LOGGER.warn("This Java Virtual Machine does not support CPU Time Measurements, "
					+ "tunerTimeout will not contain any SMAC Execution Time Information.");
		}
		
		if (options.seedOptions.numRun + options.seedOptions.seedOffset < 0) {
			LOGGER.warn("NumRun {} plus Seed Offset {} should be positive, things may not seed correctly",
					options.seedOptions.numRun, options.seedOptions.seedOffset);
		}
	}
	
	private void logSmacTermination(AbstractAlgorithmFramework smac) {
		ParameterConfiguration incumbent = smac.getIncumbent();
		RunHistory runHistory = smac.runHistory();
		TerminationCondition tc = smac.getTerminationCondition();
		
		final DecimalFormat df0 = new DecimalFormat("0");
		String callString = smac.getCallString();
		LOGGER.info(new StringBuilder("\n============================================================\n")
				.append(String.format("SMAC has finished. Reason: %s\n", smac.getTerminationReason()))
				.append(String.format("Total number of runs performed: %d, total configurations tried: %d.\n",
						runHistory.getAlgorithmRunsIncludingRedundant().size(),
						runHistory.getAllParameterConfigurationsRan().size()))
				.append(String.format("Total CPU time used: %s s, total wallclock time used: %s s.\n",
						df0.format(tc.getTunerTime()), df0.format(tc.getWallTime())))
				.append(String.format("SMAC's final incumbent: config %d (internal ID: %s, args), ",
						runHistory.getThetaIdx(incumbent), incumbent.toString()))
				.append(String.format("with estimated %s: %s, ",
						smac.getObjectiveToReport(), df0.format(smac.getEmpericalPerformance(incumbent))))
				.append(String.format("based on %d run(s) on %d training instance(s).\n",
						runHistory.getAlgorithmRunsExcludingRedundant(incumbent).size(),
						runHistory.getProblemInstancesRan(incumbent).size()))
				.append(String.format("Sample call for this final incumbent:\n%s\n", callString.trim()))
				.toString());
	}
}
