#!/bin/bash

echo -e "\nbuild docker ambari server node\n"
sudo docker build -t "dockerfile/ubuntu14.04:ambari-server" .

sudo docker images
