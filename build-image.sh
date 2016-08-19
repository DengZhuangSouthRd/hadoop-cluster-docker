#!/bin/bash

echo -e "\nbuild docker hadoop image\n"
sudo docker build -t "dockerfile/ubuntu14.04:java" .

sudo docker images
