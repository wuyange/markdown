# flannel网络

​		`flannel` 是 `CoreOS` 开发的容器网络解决方案。`flannel` 为每个 `host` 分配一个 `subnet`，容器从此 `subnet` 中分配 `IP`，这些 `IP` 可以在主机间路由，容器间无需 `NAT` 和 `port mapping` 就可以跨主机通信。

​		每个`subnet`都是从一个更大的`IP`池中划分的，`flannel`会在每个主机上运行一个叫`flanncld` 的`agent`，其职责就是从池子中分配`subnet`。为了在各个主机间共享信息，`flannel` 用`etcd` 存放网络配置、已分配的 `subnet`、`host`的 `IP`等信息。数据包如何在主机间转发是由`backend` 实现的。`flannel` 提供了多种 `backend`，最常用的有`vxlan`和`host-gw` 

## 实验环境搭建

### 安装etcd

```shell
yum -y install etcd flannel

# 启动etcd并打开2379监听端口
etcd -listen-client-urls http://10.182.81.24:2379 -advertise-client-urls http://10.182.81.24:2379 &

# 测试etcd是否可用
[root@centos7 ~]# etcdctl --endpoints=http://10.182.81.24:2379 set foo "bar"
bar
[root@centos7 ~]# etcdctl --endpoints=http://10.182.81.24:2379 get foo
bar
```

### 安装flannel

```shell
# ubuntu
# ftp下载到/tmp目录
ftp 10.182.79.201
# 安装flannel
apt install /tmp/flannel_0.9.1_ds1-1_amd64.deb

# centos
yum install -y flannel
```

### 将flannel网络配置信息保存到etcd

```shell
[root@centos7 ~]# etcdctl --endpoints http://10.182.81.24:2379 set /docker-test/network/config  '{"Network": "10.2.0.0/16", "SubnetLen": 24, "Backend": {"Type": "vxlan"}}'
{"Network": "10.2.0.0/16", "SubnetLen": 24, "Backend": {"Type": "vxlan"}}
[root@centos7 ~]# etcdctl --endpoints=http://10.182.81.24:2379 get /docker-test/network/config
{"Network": "10.2.0.0/16", "SubnetLen": 24, "Backend": {"Type": "vxlan"}}
# Network定义该网络的IP池为10.2.0.0、15
# SubnetLen指定每个主机分配道德subnet大小为24位
# Backend位vxlan，即主机间通过vxlan通信
# /docker-test/network/config是此etcd数据项的key
```

### 启动flannel

```shell
flanneld -etcd-endpoints=http://10.182.81.24:2379 -iface=ens160 -etcd-prefix=/docker-test/network

# -etcd-endpoints:指定etcd url
# -iface:指定主机间数据传输使用的interface
# -etcd-prefix:指定etcd存放flannel网络配置信息的key

# centos
[root@host2 ~]# flanneld -etcd-endpoints=http://10.182.81.24:2379 -iface=ens32 -etcd-prefix=/docker-test/network
I0714 23:09:48.794905   10062 main.go:132] Installing signal handlers
I0714 23:09:48.796355   10062 manager.go:149] Using interface with name ens32 and address 10.182.243.64
I0714 23:09:48.796422   10062 manager.go:166] Defaulting external address to interface address (10.182.243.64)
I0714 23:09:48.859168   10062 local_manager.go:179] Picking subnet in range 10.2.1.0 ... 10.2.255.0
I0714 23:09:48.872496   10062 manager.go:250] Lease acquired: 10.2.6.0/24
I0714 23:09:48.873250   10062 network.go:58] Watching for L3 misses
I0714 23:09:48.873303   10062 network.go:66] Watching for new subnet leases
# ens32被选作与外部主机通信的interface
# 识别flannel网络池10.2.0.0/16
# 分配的subnet为10.2.6.0/24

# flanneld启动后，一个新的interface flannel.1被创建，而且配置上的第一个ip 10.2.6.0
[root@host2 ~]# ip addr show flannel.1
10: flannel.1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1450 qdisc noqueue state UNKNOWN group default
    link/ether ee:97:5b:60:7c:69 brd ff:ff:ff:ff:ff:ff
    inet 10.2.6.0/32 scope global flannel.1
       valid_lft forever preferred_lft forever
    inet6 fe80::ec97:5bff:fe60:7c69/64 scope link
       valid_lft forever preferred_lft forever
# host上添加了一条路由，目的地址位flannel网络的10.2.0.0、16的数据都由flannel.1转发
[root@host2 ~]# ip route
default via 10.182.243.1 dev ens32 proto static metric 100
10.2.0.0/16 dev flannel.1
10.182.243.0/24 dev ens32 proto kernel scope link src 10.182.243.64 metric 100
10.192.168.0/24 dev br-2607c1228a0e proto kernel scope link src 10.192.168.1
172.17.0.0/16 dev docker0 proto kernel scope link src 172.17.0.1
172.18.0.0/16 dev br-dd302a5565f1 proto kernel scope link src 172.18.0.1
192.168.122.0/24 dev virbr0 proto kernel scope link src 192.168.122.1


# ubuntu
[root@host2 ~]# flannel -etcd-endpoints=http://10.182.81.24:2379 -iface=ens160 -etcd-prefix=/docker-test/network
ERROR: logging before flag.Parse: I0714 21:43:36.544326   21620 main.go:487] Using interface with name ens160 and address 10.182.79.36
ERROR: logging before flag.Parse: I0714 21:43:36.544381   21620 main.go:504] Defaulting external address to interface address (10.182.79.36)
ERROR: logging before flag.Parse: I0714 21:43:36.544451   21620 main.go:234] Created subnet manager: Etcd Local Manager with Previous Subnet: 0.0.0.0/0
ERROR: logging before flag.Parse: I0714 21:43:36.544462   21620 main.go:237] Installing signal handlers
ERROR: logging before flag.Parse: I0714 21:43:36.546846   21620 main.go:352] Found network config - Backend type: vxlan
ERROR: logging before flag.Parse: I0714 21:43:36.546898   21620 vxlan.go:119] VXLAN config: VNI=1 Port=0 GBP=false DirectRouting=false
ERROR: logging before flag.Parse: I0714 21:43:36.677090   21620 local_manager.go:234] Picking subnet in range 10.2.1.0 ... 10.2.255.0
ERROR: logging before flag.Parse: I0714 21:43:36.678427   21620 local_manager.go:220] Allocated lease (10.2.76.0/24) to current node (10.182.79.36)
ERROR: logging before flag.Parse: I0714 21:43:36.679080   21620 main.go:299] Wrote subnet file to /run/flannel/subnet.env
ERROR: logging before flag.Parse: I0714 21:43:36.679096   21620 main.go:303] Running backend.
ERROR: logging before flag.Parse: I0714 21:43:36.679243   21620 vxlan_network.go:56] watching for new subnet leases
ERROR: logging before flag.Parse: I0714 21:43:36.680843   21620 main.go:395] Waiting for 23h0m0.037888798s to renew lease
ERROR: logging before flag.Parse: I0714 21:43:36.684567   21620 iptables.go:114] Some iptables rules are missing; deleting and recreating rules
ERROR: logging before flag.Parse: I0714 21:43:36.684591   21620 iptables.go:136] Deleting iptables rule: -s 10.2.0.0/16 -j ACCEPT
ERROR: logging before flag.Parse: I0714 21:43:36.685990   21620 iptables.go:136] Deleting iptables rule: -d 10.2.0.0/16 -j ACCEPT
ERROR: logging before flag.Parse: I0714 21:43:36.687326   21620 iptables.go:124] Adding iptables rule: -s 10.2.0.0/16 -j ACCEPT
ERROR: logging before flag.Parse: I0714 21:43:36.690099   21620 iptables.go:124] Adding iptables rule: -d 10.2.0.0/16 -j ACCEPT
```

当前拓扑

![image-20220714232611888](https://gitee.com/shunyu-online/shunyu_typora_image/raw/master/image/image-20220714232611888.png)

## 配置docker连接flannel

编辑`10.182.81.24`的`docker`配置文件`/usr/lib/systemd/system/docker.service(centos)`，设置`--bip`和`--mtu`和`/run/flannel/subnet.env`中的内容一致

```shell
[root@centos7 system]# cat /run/flannel/subnet.env
FLANNEL_NETWORK=10.2.0.0/16
FLANNEL_SUBNET=10.2.13.1/24
FLANNEL_MTU=1450
FLANNEL_IPMASQ=false

# vi docker.service
ExecStart=/usr/bin/dockerd -H fd:// --containerd=/run/containerd/containerd.sock --bip=10.2.13.1/24 --mtu=1450

# 重启docker服务
systemctl daemon-reload
systemctl restart docker

# docker会将10.2.13.1配置到Linux bridge docker0上，并添加10.2.13.0/24的路由
[root@centos7 system]# ip route
default via 10.182.81.1 dev ens192 proto static metric 100
10.2.0.0/16 dev flannel.1
10.2.13.0/24 dev docker0 proto kernel scope link src 10.2.13.1
10.182.81.0/24 dev ens192 proto kernel scope link src 10.182.81.24 metric 100

# 在10.182.243.64执行相同的操作
# flannel没有创建新的docker网络，而是直接使用默认的bridge网络，同一主机的容器通过docker0连接，跨主机浏览通过flannel.1转发
```

### flannel网络连通性

将容器连接到`flannel`网络

```shell
 # 两台host执行
 docker run -itd --name bbox1 busybox
```

`host-gw` 和 `vxlan`简单比较。

- `host-gw`把每个主机都配置成网关，主机知道其他主机的`subnet`和转发地址。`vxlan`则在主机间建立隧道，不同主机的容器都在一个大的网段内
- 虽然 `vxlan`与`host-gw`使用不同的机制建立主机之间连接，但对于容器则无须任何改变
- 由于`vxlan`需要对数据进行额外打包和拆包，性能会稍逊于`host-gw.`





