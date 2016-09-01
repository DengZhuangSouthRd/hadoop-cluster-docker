#!/bin/bash

CURPATH=`pwd`
CONTAINER_HOSTS=${CURPATH}/docker-container-hosts

if [ $# = 0 ]
then
	echo "Please specify the node number of hadoop cluster!"
	exit 1
fi

startDockerCluster() {
    sudo docker rm -f `sudo docker ps -a -q`

    N=$1

    i=1
    while [ $i -le $N ]
    do
        echo "start hadoop-slave$i container..."
        sudo docker run -itd \
                        --net=hadoop \
                        --name hadoop-slave$i \
                        --hostname hadoop-slave$i \
                        -v /opt/hadoop/slave$i/datanode:/root/hdfs/datanode \
                        -v /opt/hadoop/slave$i/namenode:/root/hdfs/namenode \
                        dockerfile/ubuntu14.04:hadoop > /dev/null
        i=$(( $i + 1 ))
    done 

    # start hadoop master container
    echo "start hadoop-master container..."
    sudo docker run -itd \
                    --net=hadoop \
                    -p 50070:50070 \
                    -p 8088:8088 \
                    -p 19888:19888 \
                    -p 10020:10020 \
                    --name hadoop-master \
                    --hostname hadoop-master \
                    -v /opt/hadoop/master/datanode:/root/hdfs/datanode \
                    -v /opt/hadoop/master/namenode:/root/hdfs/namenode \
                    dockerfile/ubuntu14.04:hadoop > /dev/null
}

startDockerCluster $1
sudo docker ps -a
sudo docker exec -it hadoop-master /bin/bash
