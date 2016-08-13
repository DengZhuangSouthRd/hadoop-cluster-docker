#!/bin/bash

# kill already run docker
sudo docker rm -f `sudo docker ps -a -q`

# the default node number is 3
N=${1:-3}

# start hadoop slave container
i=1
while [ $i -lt $N ]
do
	echo "start hadoop-slave$i container..."
	sudo docker run -itd \
	                --net=hadoop \
	                --name hadoop-slave$i \
	                --hostname hadoop-slave$i \
                    -v /opt/hadoop/slave$i/datanode:/root/hdfs/datanode \
                    -v /opt/hadoop/slave$i/namenode:/root/hdfs/namenode \
                    kiwenlau/hadoop:1.0 &> /dev/null
	i=$(( $i + 1 ))
done 

# start hadoop master container
echo "start hadoop-master container..."
sudo docker run -itd \
                --net=hadoop \
                -p 50070:50070 \
                -p 8088:8088 \
                --name hadoop-master \
                --hostname hadoop-master \
                -v /opt/hadoop/master/datanode:/root/hdfs/datanode \
                -v /opt/hadoop/master/namenode:/root/hdfs/namenode \
                kiwenlau/hadoop:1.0 &> /dev/null



sudo docker ps -a
# get into hadoop master container
sudo docker exec -it hadoop-master bash
