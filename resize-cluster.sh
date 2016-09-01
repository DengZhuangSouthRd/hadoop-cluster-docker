#!/bin/bash

# N is the node number of hadoop cluster

if [ $# = 0 ]
then
	echo "Please specify the node number of hadoop cluster!"
	exit 1
fi

# change slaves file
changeNodeNums() {
    Num=$1
    echo "Chang Hadoop Slave numberbers !"
    if [ -e config/slaves ];then
        rm config/slaves
    fi
    i=1
    while [ $i -le $Num ]
    do
        echo "hadoop-slave${i}" >> config/slaves
        i=$(($i+1))
    done
}

removeImage() {
    echo "Before create, we should clear the exists hadoop !"
    sudo docker images | grep "hadoop" | awk -F' ' '{ print $3 }'
    if [ $? -ne 0 ];then
        return 1
    else
        imagesid=`sudo docker images | grep "hadoop" | awk -F' ' '{ print $3 }'`
        sudo docker rmi -f ${imagesid}
        return 0
    fi
}

N=$1
echo -e "\nbuild docker hadoop image\n"
changeNodeNums ${N}
removeImage
sudo docker build -t "dockerfile/ubuntu14.04:hadoop" .
sudo docker images
