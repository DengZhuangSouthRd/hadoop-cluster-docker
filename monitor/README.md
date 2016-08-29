# 对Hadoop集群中，每个节点的不同控制方案

---

## 启动顺序
- 先启动服务器，获取启动的docker的IP和hostname
- 将获取的信息发送给外部控制server
- 同时将自己的标志标记为Master节点
- 将Master节点的key发送给外部控制节点
- 其他slave节点可以通过通信协议，将自己的数据打包成相应的格式传递到控制节点中

## 每个节点的配置
- 每个Docker都是一个客户端，其中具有Master属性的节点是Hadoop集群中的Master节点
- 配置各个节点的免密码链接登录
```bash
$ ssh-copy-id hadoop@slave1.hadoop.com
$ ssh hadoop@slave1.hadoop.com

# 如果没有发现ssh-copy-id命令，可以手动的配置如下命令

$ cat ~/.ssh/id_rsa.pub | ssh hadoop@slave1.hadoop.com 'cat >> ~/.ssh/authorized_keys'
＃ 上述命令等于如下两个命令
$ scp ~/.ssh/id_rsa.pub hadoop@slave1.hadoop.com:/tmp
$ cat /tmp/id_rsa.pub >> ~/.ssh/authorized_keys

＃ 测试一下
$ ssh hadoop@slave1.hadoop.com
```
- 同时也要保证各个节点之间的通信是完整的，除了本身的ssh-key之外，其他节点的ssh-key都要加入到本地的主机的authorized_keys中去

## 外部控制节点和每个docker节点之间的通信协议
### 客户端
- 发送信息的格式
```bash
{
    "role" : "slave" | "master",
    "is_alive":"True"|"False",
    "hostname": "slave1.hadoop.com",
    "ip":"192.168.0.2",
    "id_rsa.pub" : "xxxxxx",
    "username" : "hadoop",
}
use format:
    info_dict = {}
    info_str = json.dumps(info_dict)
    socket.send(info_str)
```
- 客户端，还可以按时发送心跳包给服务器，告诉服务器工作是否正常
```bash
{
    "role" : "slave" | "master",
    "is_alive":"True"|"False",
    "hostname": "slave1.hadoop.com",
    "ip":"192.168.0.2",
    "type" : "heartbeat",
    "username" : "hadoop",
}
use format:
    info_dict = {}
    info_str = json.dumps(info_dict)
    socket.send(info_str)
```

### 服务器
- 服务器打开50091端口，接收信息
- 每当服务器接到信息后，回给对应节点发送相应的ACK确认信息
- 服务器也会主动发送给各个节点相应的集群的状态信息，数据格式如下：
```bash
{
    "role" : "server",
    "is_alive" : "True" | "False",
    "hostname" : "server.hadoop.com",
    "ip" : "10.2.3.119",
    "username" : "root",
    "id_rsa.pub" : "xxxxxx",
    "clusers_ip" : [(ip, hostname),(ip, hostname),...,(ip, hostname)],
    "clusers_ssh" : [(hostname, ssh-key),(hostname, ssh-key),(hostname, ssh-key)]
}
use format:
    info_dict = {}
    info_str = json.dumps(info_dict)
    socket.send(info_str)
```
- 客户端接到数据后，回返回给服务器相应的状态信息，进行确认
```bash
{
    "role" : "server",
    "is_alive" : "True" | "False",
    "hostname" : "server.hadoop.com",
    "ip" : "10.2.3.119",
    "username" : "root",
    "type" : "heartbeat"
}
use format:
    info_dict = {}
    info_str = json.dumps(info_dict)
    socket.send(info_str)
```
- 服务器给客户端发送的其他形式的数据
  - type : update(主要是针对集群中各个节点的状态发生了更新，使用类型的数据，可以使得client节点，更新配置信息)
  ```bash
    {
        "role" : "server",
        "is_alive" : "True" | "False",
        "hostname" : "server.hadoop.com",
        "ip" : "10.2.3.119",
        "username" : "root",
        "type" : "update",
        "clusers_ip" : [(ip, hostname),(ip, hostname),...,(ip, hostname)],
        "clusers_ssh" : [(hostname, ssh-key),(hostname, ssh-key),(hostname, ssh-key)]
    }
    use format:
        info_dict = {}
        info_str = json.dumps(info_dict)
        socket.send(info_str)
  ```
