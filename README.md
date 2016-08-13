##Run Hadoop Cluster within Docker Containers

- Blog: [Run Hadoop Cluster in Docker Update](http://kiwenlau.com/2016/06/26/hadoop-cluster-docker-update-english/)
- 博客: [基于Docker搭建Hadoop集群之升级版](http://kiwenlau.com/2016/06/12/160612-hadoop-cluster-docker-update/)

- 源使用Docker搭建集群，没有办法处理一个问题，就是每个hadoop节点的IP是由Docker启动之后采用DHCP的方案确定的！
- 给出解决方案(1)
> 对于每个启动的Docker，我们都可以使用 **sudo docker inspect -format={{.xxxx.xxxxx}}** 取出指定的信息
然后由外部的某个程序将数据写入到master节点中，同时这个步骤要在启动Hadoop集群的之前完成操作

- 给出解决方案(2)
> 对于每个启动的Docker，我们写一个内部程序，该程序的主要用户是获取主机的主机名和IP地址，之后将某个信息发送到指定的外部服务器中，
通过外部服务器的信息汇集之后，统一写入到master节点中的对应位置

- 在每个Docker中使用这个命令可以很好的获取IP和HostName
```
root@hadoop-master:~/monitor# more host-ip.sh
#!/bin/bash

ip=`ifconfig eth0 | grep 'inet addr:' | awk -F' ' '{ print $2  }' | awk -F':' '{ print $2  }'`
name=`hostname`
echo $ip
echo $name
```

- 同时想保证所有节点可以自动的加入和退出，我们需要在外部机器中写一个后台程序，一直在监控各个节点的运行情况。

