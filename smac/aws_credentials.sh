AWS_HOME=$HOME/.aws

function access_key() {
  grep --word-regexp $2 $1 | cut --fields 2 --delimiter '=' | tr --delete [:blank:]
}

function import_aws_credentials() {
  AWS_ACCESS_KEY_ID=$(access_key $1 aws_access_key_id)
  AWS_SECRET_ACCESS_KEY=$(access_key $1 aws_secret_access_key)
}

function export_spark_credentials() {
  SPARK_PREFIX="spark.hadoop.fs.s3a"
  echo -e $SPARK_PREFIX".access.key\t\t"$AWS_ACCESS_KEY_ID >> $1
  echo -e $SPARK_PREFIX".secret.key\t\t"$AWS_SECRET_ACCESS_KEY >> $1
}




if [ -z ${SPARK_HOME+x} ]; then
  echo "SPARK_HOME is unset!"
  exit 1

else
  echo "SPARK_HOME is set to $SPARK_HOME"
  if [ ! -d $SPARK_HOME/conf ]; then
    echo "SPARK_HOME does not point to a valid Spark setup directory!"
    exit 1
  fi
fi




echo "Looking for AWS credentials in $AWS_HOME"

if [ -r $AWS_HOME/credentials ]; then
  echo "Importing AWS credentials from credentials file..."
  import_aws_credentials $AWS_HOME/credentials
elif [ -r $AWS_HOME/config ]; then
  echo "Importing AWS credentials from config file..."
  import_aws_credentials $AWS_HOME/config
else
  echo "Cannot import AWS credentials from any valid location!"
  exit 1
fi




SPARK_CONF=$SPARK_HOME/conf/spark-defaults.conf

if [ ! -r $SPARK_CONF ] && [ -r $SPARK_CONF.template ]; then
  echo "Initializing Spark configuration file from template..."
  cp $SPARK_CONF.template $SPARK_CONF
fi

echo "Exporting credentials to $SPARK_CONF"
export_spark_credentials $SPARK_CONF




wget https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk/1.7.4/aws-java-sdk-1.7.4.jar -P $SPARK_HOME/jars/
wget https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/2.7.3/hadoop-aws-2.7.3.jar -P $SPARK_HOME/jars/
wget https://repo1.maven.org/maven2/net/java/dev/jets3t/jets3t/0.9.4/jets3t-0.9.4.jar -P $SPARK_HOME/jars/
