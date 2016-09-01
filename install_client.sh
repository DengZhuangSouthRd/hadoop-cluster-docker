#!/bin/bash
if [ -d "/usr/local/src/hadoop-2.7.2" ];then
    echo "Hadoop client have already exists !"
    #exit 0
fi

if [ ! -e "hadoop-2.7.2.tar.gz" ];then
    wget https://github.com/kiwenlau/compile-hadoop/releases/download/2.7.2/hadoop-2.7.2.tar.gz
fi

tar -zxf hadoop-2.7.2.tar.gz -C/usr/local/src/
rm hadoop-2.7.2.tar.gz
echo "export PATH=/usr/local/src/hadoop-2.7.2/bin:\$PATH" >> ~/.bashrc
cd /usr/local/src/hadoop-2.7.2/etc/hadoop


