#!/bin/bash

echo "Input Master hostname:"
masterip=$(awk 'NR=='1' {print $1}' spark.txt)
echo $masterip
echo "Input Slave1 hostname:"
slaveip=$(awk 'NR=='2' {print $1}' spark.txt)
echo $slaveip
echo "Input Slave2 hostname:"
slaveip2=$(awk 'NR=='3' {print $1}' spark.txt)
echo $slaveip2
echo "Modify /usr/local/spark/conf/spark-env.sh......"
line=`sed -n "/SPARK_NICENESS/=" /usr/local/spark/conf/spark-env.sh`
sed -i "${line}aexport SPARK_DIST_CLASSPATH=$(/usr/local/hadoop/bin/hadoop classpath)\n\
export JAVA_HOME=/usr/lib/jvm/jdk\n\
export SPARK_HISTORY_OPTS=\"-Dspark.history.ui.port=18080 -Dspark.history.retainedApplications=3 -Dspark.history.fs.logDirectory=hdfs://ns1/tmp/spark-events\"\n\
#export SPARK_MASTER_IP=$masterip\n\
export SPARK_MASTER_PORT=7077\n\
export SCALA_HOME=/usr/local/scala\n\
export SPARK_HOME=/usr/local/spark\n\
export HADOOP_CONF_DIR=/usr/local/hadoop/etc/hadoop\n\
export SPARK_LIBRARY_PATH=$SPARK_HOME/lib\n\
export SPARK_LOCAL_DIRS=/mnt/disk1/tmp/spark\n\
export SCALA_LIBRARY_PATH=$SPARK_LIBRARY_PATH\n\
export PYSPARK_PYTHON=/usr/bin/python3\n\
export SPARK_DAEMON_JAVA_OPTS=\"-Dspark.deploy.recoveryMode=ZOOKEEPER -Dspark.deploy.zookeeper.url=$masterip:2181,$slaveip:2181,$slaveip2:2181 -Dspark.deploy.zookeeper.dir=/spark\" " /usr/local/spark/conf/spark-env.sh
echo "Modify /usr/local/spark/conf/spark-defaults.conf......"
line=`sed -n "/extraJavaOptions/=" /usr/local/spark/conf/spark-defaults.conf`
sed -i "${line}aspark.eventLog.enabled           true\n\
spark.eventLog.dir               hdfs://ns1/tmp/spark-events/\n\
spark.local.dir                  file:/mnt/disk1/tmp/spark/" /usr/local/spark/conf/spark-defaults.conf
echo "Modify /usr/local/spark/conf/slaves......"
line=`sed -n "/localhost/=" /usr/local/spark/conf/slaves`
sed -i "${line}a$masterip\n\
$slaveip" /usr/local/spark/conf/slaves
echo "Modify /usr/local/spark/conf/metrics.properties......"
line=`sed -n "/executor.source.jvm.class/=" /usr/local/spark/conf/metrics.properties`
sed -i "${line}amy_config=$1" /usr/local/spark/conf/metrics.properties

