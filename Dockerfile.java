FROM ubuntu:14.04

MAINTAINER liuguiyang "liuguiyangnwpu@163.com"

WORKDIR /root

RUN apt-get -qq update
RUN apt-get -qqy install openssh-server vim net-tools wget 
RUN apt-get -qqy install openjdk-7-jdk
RUN ssh-keygen -t rsa -f ~/.ssh/id_rsa -P ''
RUN cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys

ENV JAVA_HOME=/usr/lib/jvm/java-7-openjdk-amd64

# ssh without key

COPY config/ssh_config /tmp/

RUN mv /tmp/ssh_config ~/.ssh/config

CMD [ "sh", "-c", "service ssh start; bash"]
