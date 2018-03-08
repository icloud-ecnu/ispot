#!/bin/bash

namenode=$(awk 'NR=='1' {print $1}' hdfs.txt)
echo $namenode
datanode=$(awk 'NR=='2' {print $1}' hdfs.txt)
echo $datanode
datanode2=$(awk 'NR=='3' {print $1}' hdfs.txt)
echo $datanode2
check_rdd=0,1
scp /home/ubuntu/ispot/ebs.sh ubuntu@$namenode:/home/ubuntu/ispot/
scp /home/ubuntu/ispot/mountpoint ubuntu@$namenode:/home/ubuntu/ispot/

scp -r /usr/local/hadoop/etc/hadoop ubuntu@$namenode:/usr/local/hadoop/etc
scp -r /usr/local/zookeeper/conf ubuntu@$namenode:/usr/local/zookeeper
scp -r /usr/local/zookeeper/tmp ubuntu@$namenode:/usr/local/zookeeper
scp -r /usr/local/spark/conf ubuntu@$namenode:/usr/local/spark
scp /home/ubuntu/ispot/hdfs.txt ubuntu@$namenode:/home/ubuntu/ispot/
scp /home/ubuntu/ispot/hdfs.sh ubuntu@$namenode:/home/ubuntu/ispot/
scp /home/ubuntu/ispot/spark.txt ubuntu@$namenode:/home/ubuntu/ispot/
scp /home/ubuntu/ispot/spark.sh ubuntu@$namenode:/home/ubuntu/ispot/
ssh ubuntu@$namenode > /dev/null 2>&1 << eeooff
rm -r /home/ubuntu/hadoop/tmp
rm -rf /usr/local/zookeeper/tmp/version-2
cd /home/ubuntu/ispot
./ebs.sh
./hdfs.sh 1
./spark.sh $check_rdd

eeooff
expect -c "
        set timeout 5;
        spawn ssh ubuntu@$namenode -p 22 ;
        expect {
                yes/no { send \"yes\r\" }
                } ;

expect ubuntu@* { send \"cd /usr/local/zookeeper/bin \r\" } ;
expect ubuntu@* { send \"./zkServer.sh start \r\" } ;
expect ubuntu@* { send \"cd /usr/local/hadoop/sbin \r\" } ;
expect ubuntu@* { send \"./hadoop-daemon.sh start journalnode \r\" } ;
                expect ubuntu@* { send exit\r } ;
                expect eof ;
        "
#config node2
scp /home/ubuntu/ispot/ebs.sh ubuntu@$datanode:/home/ubuntu/ispot/
scp /home/ubuntu/ispot/mountpoint ubuntu@$datanode:/home/ubuntu/ispot/

scp -r /usr/local/hadoop/etc/hadoop ubuntu@$datanode:/usr/local/hadoop/etc
scp -r /usr/local/zookeeper/conf ubuntu@$datanode:/usr/local/zookeeper
scp -r /usr/local/zookeeper/tmp ubuntu@$datanode:/usr/local/zookeeper
scp -r /usr/local/spark/conf ubuntu@$datanode:/usr/local/spark
scp /home/ubuntu/ispot/hdfs.sh ubuntu@$datanode:/home/ubuntu/ispot/
scp /home/ubuntu/ispot/spark.sh ubuntu@$datanode:/home/ubuntu/ispot/
scp /home/ubuntu/ispot/hdfs.txt ubuntu@$datanode:/home/ubuntu/ispot/
scp /home/ubuntu/ispot/spark.txt ubuntu@$datanode:/home/ubuntu/ispot/
ssh ubuntu@$datanode > /dev/null 2>&1 << eeooff

rm -r /home/ubuntu/hadoop/tmp
rm -rf /usr/local/zookeeper/tmp/version-2
cd /home/ubuntu/ispot
./ebs.sh
./hdfs.sh 2
./spark.sh $check_rdd

eeooff

expect -c "
        set timeout 5;
        spawn ssh ubuntu@$datanode -p 22 ;
        expect {
                yes/no { send \"yes\r\" }
                } ;

expect ubuntu@* { send \"cd /usr/local/zookeeper/bin \r\" } ;
expect ubuntu@* { send \"./zkServer.sh start \r\" } ;
expect ubuntu@* { send \"cd /usr/local/hadoop/sbin \r\" } ;
expect ubuntu@* { send \"./hadoop-daemon.sh start journalnode \r\" } ;
                expect ubuntu@* { send exit\r } ;
                expect eof ;
        "

#config node3
scp /home/ubuntu/ispot/ebs.sh ubuntu@$datanode2:/home/ubuntu/ispot/
scp /home/ubuntu/ispot/mountpoint ubuntu@$datanode2:/home/ubuntu/ispot/

scp -r /usr/local/hadoop/etc/hadoop ubuntu@$datanode2:/usr/local/hadoop/etc
scp -r /usr/local/zookeeper/conf ubuntu@$datanode2:/usr/local/zookeeper
scp -r /usr/local/zookeeper/tmp ubuntu@$datanode2:/usr/local/zookeeper
scp -r /usr/local/spark/conf ubuntu@$datanode2:/usr/local/spark
scp /home/ubuntu/ispot/hdfs.sh ubuntu@$datanode2:/home/ubuntu/ispot/
scp /home/ubuntu/ispot/spark.sh ubuntu@$datanode2:/home/ubuntu/ispot/
scp /home/ubuntu/ispot/hdfs.txt ubuntu@$datanode2:/home/ubuntu/ispot/
scp /home/ubuntu/ispot/spark.txt ubuntu@$datanode2:/home/ubuntu/ispot/
ssh ubuntu@$datanode2 > /dev/null 2>&1 << eeooff

rm -r /home/ubuntu/hadoop/tmp
rm -rf /usr/local/zookeeper/tmp/version-2
cd /home/ubuntu/ispot
./ebs.sh
./hdfs.sh 3
./spark.sh $check_rdd

eeooff
expect -c "
        set timeout 5;
        spawn ssh ubuntu@$datanode2 -p 22 ;
        expect {
                yes/no { send \"yes\r\" }
                } ;

expect ubuntu@* { send \"cd /usr/local/zookeeper/bin \r\" } ;
expect ubuntu@* { send \"./zkServer.sh start \r\" } ;
expect ubuntu@* { send \"cd /usr/local/hadoop/sbin \r\" } ;
expect ubuntu@* { send \"./hadoop-daemon.sh start journalnode \r\" } ;
                expect ubuntu@* { send exit\r } ;
                expect eof ;
        "



echo $namenode
#format hdfs

expect -c "
	set timeout 5;
	spawn ssh ubuntu@$namenode -p 22 ;
	expect {
		yes/no { send \"yes\r\" }
		} ;
expect ubuntu@* { send \"hdfs zkfc -formatZK \r\" } ;
                expect { 
                N\) { send \"Y\r\" } } ;             
                expect { 
                connected. { send \"Y\r\" } } ;
               expect ubuntu@* { send \"hdfs namenode -format \r\" } ;
               expect { 
                N\) { send \"Y\r\" } } ;
                expect { 
                N\) { send \"Y\r\" } } ;

		expect ubuntu@* { send exit\r } ;
		expect eof ;
	"
#start Hadoop
echo $namenode
ssh ubuntu@$namenode > /dev/null 2>&1 << eeooff
rm /home/ubuntu/.ssh/known_hosts
sudo chmod 666 /etc/ssh/ssh_config
echo 'StrictHostKeyChecking no' >> /etc/ssh/ssh_config
echo 'UserKnownHostsFile /dev/null' >> /etc/ssh/ssh_config
cd /usr/local/hadoop/sbin
./start-dfs.sh
./start-yarn.sh
eeooff

#double namenode
expect -c "
        set timeout 5;
        spawn ssh ubuntu@$datanode -p 22 ;
        expect {
                yes/no { send \"yes\r\" }
                } ;
expect ubuntu@* { send \"hdfs namenode -bootstrapstandby \r\" } ;
expect { 
                N\) { send \"Y\r\" } } ;
expect ubuntu@* { send \"cd /usr/local/hadoop/sbin \r\" } ;
expect ubuntu@* { send \"./hadoop-daemon.sh start namenode \r\" } ;
                expect ubuntu@* { send exit\r } ;
                expect eof ;
        "
#start spark including master and worker
echo $namenode
ssh ubuntu@$namenode > /dev/null 2>&1 << eeooff
cd /usr/local/spark/sbin
./start-all.sh
eeooff

ssh ubuntu@$datanode > /dev/null 2>&1 << eeooff 
cd /usr/local/spark/sbin
./start-master.sh
eeooff

master="$namenode:7077"
ssh ubuntu@$datanode2 > /dev/null 2>&1 << eeooff 
cd /usr/local/spark/sbin
./start-slave.sh $master
eeooff
