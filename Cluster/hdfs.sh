#!/bin/bash

echo "Input NameNode hostname:"
#read nameip
nameip=$(awk 'NR=='1' {print $1}' hdfs.txt)
echo $nameip
echo "Input DataNode1 hostname:"
#read dataip
dataip=$(awk 'NR=='2' {print $1}' hdfs.txt)
echo $dataip
echo "Input DataNode2 hostname"
#read dataip2
dataip2=$(awk 'NR=='3' {print $1}' hdfs.txt)
echo $dataip2
echo "Modify /usr/local/hadoop/etc/hadoop/core-site.xml......"
line=`sed -n "/<configuration>/=" /usr/local/hadoop/etc/hadoop/core-site.xml`
sed -i "${line}a<property>\n\
             <name>fs.defaultFS</name>\n\
             <value>hdfs://ns1</value>\n\
</property>\n\
<property>\n\
             <name>hadoop.tmp.dir</name>\n\
             <value>/home/ubuntu/hadoop/tmp</value>\n\
             <description>Abase for other temporary directories.</description>\n\
</property>\n\
<property>\n\
    <name>ha.zookeeper.quorum</name>\n\
    <value>$nameip:2181,$dataip:2181,$dataip2:2181</value>\n\
</property>\n\
<property>\n\
   <name>fs.file.impl</name>\n\
   <value>org.apache.hadoop.fs.LocalFileSystem</value>\n\
   <description>The FileSystem for file: uris.</description>\n\
</property>\n\
<property>\n\
   <name>fs.hdfs.impl</name>\n\
   <value>org.apache.hadoop.hdfs.DistributedFileSystem</value>\n\
   <description>The FileSystem for hdfs: uris.</description>\n\
</property>" /usr/local/hadoop/etc/hadoop/core-site.xml
echo "Modify /usr/local/hadoop/etc/hadoop/hdfs-site.xml......"
line=`sed -n "/<configuration>/=" /usr/local/hadoop/etc/hadoop/hdfs-site.xml`
sed -i "${line}a<property>\n\
    <name>dfs.nameservices</name>\n\
    <value>ns1</value>\n\
</property>\n\
<property>\n\
    <name>dfs.ha.namenodes.ns1</name>\n\
    <value>nn1,nn2</value>\n\
</property>\n\
<property>\n\
    <name>dfs.namenode.rpc-address.ns1.nn1</name>\n\
    <value>$nameip:9000</value>\n\
</property>\n\
<property>\n\
    <name>dfs.namenode.http-address.ns1.nn1</name>\n\
    <value>$nameip:50070</value>\n\
</property>\n\
<property>\n\
    <name>dfs.namenode.rpc-address.ns1.nn2</name>\n\
    <value>$dataip:9000</value>\n\
</property>\n\
<property>\n\
    <name>dfs.namenode.http-address.ns1.nn2</name>\n\
    <value>$dataip:50070</value>\n\
</property>\n\
<property>\n\
    <name>dfs.namenode.shared.edits.dir</name>\n\
    <value>qjournal://$nameip:8485;$dataip:8485;$dataip2:8485/ns1</value>\n\
</property>\n\
<property>\n\
    <name>dfs.journalnode.edits.dir</name>\n\
    <value>/home/ubuntu/hadoop/journal</value>\n\
</property>\n\
<property>\n\
    <name>dfs.ha.automatic-failover.enabled</name>\n\
    <value>true</value>\n\
</property>\n\
<property>\n\
    <name>dfs.data.dir</name>\n\
    <value>/mnt/disk1/hadoop/tmp/dfs/data/node$1</value>\n\
</property>\n\
<property>\n\
    <name>dfs.client.failover.proxy.provider.ns1</name>\n\
    <value>\n\
    org.apache.hadoop.hdfs.server.namenode.ha.ConfiguredFailoverProxyProvider\n\
    </value>\n\
</property>\n\
<property>\n\
    <name>dfs.ha.fencing.methods</name>\n\
    <value>\n\
    sshfence\n\
    shell(/bin/true)\n\
    </value>\n\
</property>\n\
<property>\n\
    <name>dfs.ha.fencing.ssh.private-key-files</name>\n\
    <value>/home/ubuntu/.ssh/id_rsa</value>\n\
</property>\n\
<property>\n\
    <name>dfs.ha.fencing.ssh.connect-timeout</name>\n\
    <value>30000</value>\n\
</property>" /usr/local/hadoop/etc/hadoop/hdfs-site.xml
echo "Modify /usr/local/hadoop/etc/hadoop/mapred-site.xml......"
line=`sed -n "/<configuration>/=" /usr/local/hadoop/etc/hadoop/mapred-site.xml`
sed -i "${line}a<property>\n\
		<name>mapreduce.framework.name</name>\n\
		<value>yarn</value>\n\
	</property>\n\
	<property>\n\
		<name>mapreduce.jobhistory.address</name>\n\
		<value>$nameip:10020</value>\n\
	</property>\n\
	<property>\n\
		<name>mapreduce.jobhistory.webapp.address</name>\n\
		<value>$nameip:19888</value>\n\
	</property>" /usr/local/hadoop/etc/hadoop/mapred-site.xml
echo "Modify /usr/local/hadoop/etc/hadoop/yarn-site.xml......"
line=`sed -n "/<configuration>/=" /usr/local/hadoop/etc/hadoop/yarn-site.xml`
sed -i "${line}a<property>\n\
		<name>yarn.nodemanager.aux-services</name>\n\
		<value>mapreduce_shuffle</value>\n\
	</property>\n\
	<property>\n\
		<name>yarn.nodemanager.aux-services.mapreduce.shuffle.class</name>\n\
		<value>org.apache.hadoop.mapred.ShuffleHandler</value>\n\
	</property>\n\
	<property>\n\
		<name>yarn.resourcemanager.address</name>\n\
		<value>$nameip:8032</value>\n\
	</property>\n\
	<property>\n\
		<name>yarn.resourcemanager.scheduler.address</name>\n\
		<value>$nameip:8030</value>\n\
	</property>\n\
	<property>\n\
		<name>yarn.resourcemanager.resource-tracker.address</name>\n\
		<value>$nameip:8035</value>\n\
	</property>\n\
	<property>\n\
		<name>yarn.resourcemanager.admin.address</name>\n\
		<value>$nameip:8033</value>\n\
	</property>\n\
	<property>\n\
		<name>yarn.resourcemanager.webapp.address</name>\n\
		<value>$nameip:8088</value>\n\
	</property>\n" /usr/local/hadoop/etc/hadoop/yarn-site.xml
echo "Modify /usr/local/hadoop/etc/hadoop/yarn-env.sh......"
line=`sed -n "/export YARN_CONF_DIR=/=" /usr/local/hadoop/etc/hadoop/yarn-env.sh`
sed -i "${line}aexport JAVA_HOME=/usr/lib/jvm/jdk" /usr/local/hadoop/etc/hadoop/yarn-env.sh
echo "Modify /usr/local/hadoop/etc/hadoop/slaves......"
line=`sed -n "/localhost/=" /usr/local/hadoop/etc/hadoop/slaves`
sed -i "${line}a$nameip\n\
$dataip\n\
$dataip2" /usr/local/hadoop/etc/hadoop/slaves
echo "Modify /usr/local/zookeeper/conf/zoo.cfg"
line=`sed -n "/dataDir=\/usr/=" /usr/local/zookeeper/conf/zoo.cfg`
sed -i "${line}aserver.1=$nameip:2888:3888\n\
server.2=$dataip:2888:3888\n\
server.3=$dataip2:2888:3888" /usr/local/zookeeper/conf/zoo.cfg
echo $1 > /usr/local/zookeeper/tmp/myid
echo "Configuration Complete!"

#cd /usr/local/zookeeper/bin
#./zkServer.sh start

#cd /usr/local/hadoop/sbin
#./hadoop-daemon.sh start journalnode
