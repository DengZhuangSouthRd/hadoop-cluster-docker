FROM ubuntu:14.04

MAINTAINER liuguiyang "liuguiyangnwpu@163.com"

WORKDIR /root

RUN apt-get -qq update
RUN apt-get -qqy install openssh-server vim net-tools wget 
RUN ssh-keygen -t rsa -f ~/.ssh/id_rsa -P ''
RUN cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys

COPY config/ssh_config /tmp/
RUN mv /tmp/ssh_config ~/.ssh/config

RUN cd /etc/apt/sources.list.d/ && wget http://public-repo-1.hortonworks.com/ambari/ubuntu14/2.x/updates/2.2.2.0/ambari.list
RUN apt-key adv --recv-keys --keyserver keyserver.ubuntu.com B9733A7A07513CAD \
        apt-get update \
        apt-get install ambari-server \
        ambari-server setup 

RUN ambari-server start

CMD [ "sh", "-c", "service ssh start; bash"]
