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
### 服务器
