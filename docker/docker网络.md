# docker网络

- `docker`安装时会自动在host上创建三个网络，可以使用`docker network ls`查看

```
root@ubuntu:/home/yushun/docker_dockerFile# docker network ls
NETWORK ID     NAME      DRIVER    SCOPE
c762b947398f   bridge    bridge    local
3d98705585a9   host      host      local
d668adc27df1   none      null      local
```

## none网络

- `none`网络就是什么都没有的网络，挂在这个网络下的容器只有lo，没有其他任何网卡，创建容器时，可以通过 `--network=none`  指定使用 `none`网络

```shell
root@ubuntu:/home/yushun/docker_dockerFile# docker run -it --network=none busybox
Unable to find image 'busybox:latest' locally
latest: Pulling from library/busybox
50e8d59317eb: Pull complete
Digest: sha256:d2b53584f580310186df7a2055ce3ff83cc0df6caacf1e3489bff8cf5d0af5d8
Status: Downloaded newer image for busybox:latest
/ # ifconfig
lo        Link encap:Local Loopback
          inet addr:127.0.0.1  Mask:255.0.0.0
          UP LOOPBACK RUNNING  MTU:65536  Metric:1
          RX packets:0 errors:0 dropped:0 overruns:0 frame:0
          TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1
          RX bytes:0 (0.0 B)  TX bytes:0 (0.0 B)

/ #
```

## host 网络

- 可以通过`--network=host`指定host网络，容器的网络配置与host完全一致。

- 使用`docker host`的网络最大的好处就是性能

```
root@ubuntu:/home/yushun/docker_dockerFile# docker run -it --network=host busybox
/ # ifconfig
docker0   Link encap:Ethernet  HWaddr 02:42:B4:F2:CE:69
          inet addr:172.17.0.1  Bcast:172.17.255.255  Mask:255.255.0.0
          inet6 addr: fe80::42:b4ff:fef2:ce69/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:4231392 errors:0 dropped:0 overruns:0 frame:0
          TX packets:4735145 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0
          RX bytes:920765260 (878.1 MiB)  TX bytes:3572287598 (3.3 GiB)

ens160    Link encap:Ethernet  HWaddr 00:0C:29:41:FA:B3
          inet addr:10.182.79.36  Bcast:10.182.79.255  Mask:255.255.255.0
          inet6 addr: fe80::20c:29ff:fe41:fab3/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:6673774 errors:0 dropped:268 overruns:0 frame:0
          TX packets:5905060 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000
          RX bytes:5695752465 (5.3 GiB)  TX bytes:689838496 (657.8 MiB)

lo        Link encap:Local Loopback
          inet addr:127.0.0.1  Mask:255.0.0.0
          inet6 addr: ::1/128 Scope:Host
          UP LOOPBACK RUNNING  MTU:65536  Metric:1
          RX packets:25974 errors:0 dropped:0 overruns:0 frame:0
          TX packets:25974 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1
          RX bytes:2620541 (2.4 MiB)  TX bytes:2620541 (2.4 MiB)
```

## bridge 网络

- docker安装时会创建一个命名为docker0的`Linux bridge`

- 不指定`--network`时，创建的容器都会默认挂在docker0上

```
root@ubuntu:/home/yushun/docker_dockerFile# brctl show
bridge name     bridge id               STP enabled     interfaces
docker0         8000.0242b4f2ce69       no              veth67a7065
                                                        vethc95ed35
```

- 使用`docker inspect bridge`可以查看docker bridge的网络配置和容器的网络配置

```
root@ubuntu:/home/yushun/6205# docker inspect bridge
[
    {
        "Name": "bridge",
        "Id": "c762b947398f8c7da843a57d2a0785f75842e52318c91ee31827a9833fb4bde6",
        "Created": "2022-05-06T02:53:24.278459374+08:00",
        "Scope": "local",
        "Driver": "bridge",
        "EnableIPv6": false,
        "IPAM": {
            "Driver": "default",
            "Options": null,
            "Config": [
                {
                    "Subnet": "172.17.0.0/16",
                    "Gateway": "172.17.0.1"
                }
            ]
        },
        "Internal": false,
        "Attachable": false,
        "Ingress": false,
        "ConfigFrom": {
            "Network": ""
        },
        "ConfigOnly": false,
        "Containers": {
            "1419b9c64c48e6d71319c2fd2bcaac1dc629ec4e775b3a93cb71dd6e22442b8d": {
                "Name": "elk",
                "EndpointID": "53751e271cb6e88d0a53834accfd62bc55275019c95b64f52c9765ad8436a963",
                "MacAddress": "02:42:ac:11:00:02",
                "IPv4Address": "172.17.0.2/16",
                "IPv6Address": ""
            },
            "d4156c3dc5646d4e614e345e1f6d973d063a79e090213b69d1158c08fb9ee561": {
                "Name": "sweet_tharp",
                "EndpointID": "1d422ecbe313d7ce423abe4ac84b5b3ef88f310247d0ce0bdc1e39679d2bdc30",
                "MacAddress": "02:42:ac:11:00:04",
                "IPv4Address": "172.17.0.4/16",
                "IPv6Address": ""
            }
        },
        "Options": {
            "com.docker.network.bridge.default_bridge": "true",
            "com.docker.network.bridge.enable_icc": "true",
            "com.docker.network.bridge.enable_ip_masquerade": "true",
            "com.docker.network.bridge.host_binding_ipv4": "0.0.0.0",
            "com.docker.network.bridge.name": "docker0",
            "com.docker.network.driver.mtu": "1500"
        },
        "Labels": {}
    }
]

```

![image-20220513121227531](C:\Users\shunyu\AppData\Roaming\Typora\typora-user-images\image-20220513121227531.png)

## user-defined网络

创建自定义的网络可以使用`user-defined`网络，`docker`提供三种`user-defined`网络驱动：`bridge`、`overlay`和`macvlan`，其中`overlay`和`macvlan`用于创建跨主机的网络

```
root@ubuntu:~# docker network create --driver bridge my_net
232d3cfcfdcb0c492d021ae5be5af31698654e6f4e0215bd446adec39a8601c0

root@ubuntu:~# brctl show
bridge name     bridge id               STP enabled     interfaces
br-232d3cfcfdcb         8000.0242e194eea8       no
docker0         8000.0242b4f2ce69       no              veth67a7065
                                                        vethc95ed35
                                                        
#新增了一个网桥br-232d3cfcfdcb,232d3cfcfdcb是新建bridge网络的短id
#使用docker network inspect xxxx 查看新建子网的配置信息
root@ubuntu:~# docker network inspect my_net
[
    {
        "Name": "my_net",
        "Id": "232d3cfcfdcb0c492d021ae5be5af31698654e6f4e0215bd446adec39a8601c0",
        "Created": "2022-05-19T19:17:23.185878565+08:00",
        "Scope": "local",
        "Driver": "bridge",
        "EnableIPv6": false,
        "IPAM": {
            "Driver": "default",
            "Options": {},
            "Config": [
                {
                    "Subnet": "172.18.0.0/16",
                    "Gateway": "172.18.0.1"
                }
            ]
        },
        "Internal": false,
        "Attachable": false,
        "Ingress": false,
        "ConfigFrom": {
            "Network": ""
        },
        "ConfigOnly": false,
        "Containers": {},
        "Options": {},
        "Labels": {}
    }
]

#可以使用--subnet 参数指定IP网段 --gateway参数指定网关
root@ubuntu:~# docker network create --driver bridge --subnet 192.168.0.0/24 --gateway 192.168.0.1  my_net_1
30fb2111e32035815c60f5c4dcc8b3eb9a45665a2e8fad6a0097b9de266c47cc
root@ubuntu:~# docker network inspect my_net_1
[
    {
        "Name": "my_net_1",
        "Id": "30fb2111e32035815c60f5c4dcc8b3eb9a45665a2e8fad6a0097b9de266c47cc",
        "Created": "2022-05-19T19:24:20.088054635+08:00",
        "Scope": "local",
        "Driver": "bridge",
        "EnableIPv6": false,
        "IPAM": {
            "Driver": "default",
            "Options": {},
            "Config": [
                {
                    "Subnet": "192.168.0.0/24",
                    "Gateway": "192.168.0.1"
                }
            ]
        },
        "Internal": false,
        "Attachable": false,
        "Ingress": false,
        "ConfigFrom": {
            "Network": ""
        },
        "ConfigOnly": false,
        "Containers": {},
        "Options": {},
        "Labels": {}
    }
]


#容器要使用自定义的网络，需要在启动时通过 --network 指定
root@ubuntu:~# docker run -it --network=my_net_1 busybox
/ # ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue qlen 1
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
26946: eth0@if26947: <BROADCAST,MULTICAST,UP,LOWER_UP,M-DOWN> mtu 1500 qdisc noqueue
    link/ether 02:42:c0:a8:00:02 brd ff:ff:ff:ff:ff:ff
    inet 192.168.0.2/24 brd 192.168.0.255 scope global eth0
       valid_lft forever preferred_lft forever


#容器启动时可以通过 --ip指定静态ip
root@ubuntu:~# docker run -it --network=my_net_1 --ip 192.168.0.2 busybox
/ # ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue qlen 1
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
26948: eth0@if26949: <BROADCAST,MULTICAST,UP,LOWER_UP,M-DOWN> mtu 1500 qdisc noqueue
    link/ether 02:42:c0:a8:00:02 brd ff:ff:ff:ff:ff:ff
    inet 192.168.0.2/24 brd 192.168.0.255 scope global eth0
       valid_lft forever preferred_lft forever
/ #


#指定重复ip时会报错
root@ubuntu:~# docker run -it --network=my_net_1 --ip 192.168.0.2 busybox
docker: Error response from daemon: Address already in use.
ERRO[0000] error waiting for container: context canceled

#只有使用--subnet创建的网络才能指定静态ip
root@ubuntu:~# docker run -it --network=my_net --ip 172.18.0.5 busybox
docker: Error response from daemon: user specified IP address is supported only when connecting to networks with user configured subnets.
ERRO[0000] error waiting for container: context canceled


#使用docker run -it --network=my_net_1 --ip 192.168.0.2 busybox
#和docker run -it --network=my_net_1 --ip 192.168.0.3 busybox创建两个容器，此时两个容器可以相互通信
root@ubuntu:~# docker run -it --network=my_net_1 --ip 192.168.0.3 busybox
/ # ping 192.168.0.2
PING 192.168.0.2 (192.168.0.2): 56 data bytes
64 bytes from 192.168.0.2: seq=0 ttl=64 time=0.234 ms
64 bytes from 192.168.0.2: seq=1 ttl=64 time=0.103 ms
64 bytes from 192.168.0.2: seq=2 ttl=64 time=0.091 ms
^C
--- 192.168.0.2 ping statistics ---
3 packets transmitted, 3 packets received, 0% packet loss
round-trip min/avg/max = 0.091/0.142/0.234 ms

#但是和docker run -it --network=my_net busybox并不能相互通信

root@ubuntu:~# docker run -it --network=my_net busybox
/ # ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue qlen 1
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
26954: eth0@if26955: <BROADCAST,MULTICAST,UP,LOWER_UP,M-DOWN> mtu 1500 qdisc noqueue
    link/ether 02:42:ac:12:00:02 brd ff:ff:ff:ff:ff:ff
    inet 172.18.0.2/16 brd 172.18.255.255 scope global eth0
       valid_lft forever preferred_lft forever
/ # ping 192.168.0.2
PING 192.168.0.2 (192.168.0.2): 56 data bytes
^C
--- 192.168.0.2 ping statistics ---
3 packets transmitted, 0 packets received, 100% packet loss


#ip r 查看host路由表
#sysctl net.ipv4.ip_forward 查看ip forwarding是否启用
#iptables-save 查看iptables
-A DOCKER-ISOLATION-STAGE-1 -i br-30fb2111e320 ! -o br-30fb2111e320 -j DOCKER-ISOLATION-STAGE-2
-A DOCKER-ISOLATION-STAGE-1 -i br-232d3cfcfdcb ! -o br-232d3cfcfdcb -j DOCKER-ISOLATION-STAGE-2
#发现iptables drop掉了网桥br-30fb2111e320和br-232d3cfcfdcb之间的流量（和书上的不太一样）
```

![image-20220519211049004](C:\Users\shunyu\AppData\Roaming\Typora\typora-user-images\image-20220519211049004.png)

```
#docker network connect my_net 57c123fb1422
#重新ping my_net网络
/ # ping 172.18.0.2
PING 172.18.0.2 (172.18.0.2): 56 data bytes
64 bytes from 172.18.0.2: seq=0 ttl=64 time=0.245 ms
64 bytes from 172.18.0.2: seq=1 ttl=64 time=0.100 ms
64 bytes from 172.18.0.2: seq=2 ttl=64 time=0.085 ms
^C
--- 172.18.0.2 ping statistics ---
3 packets transmitted, 3 packets received, 0% packet loss
#查看容器57c123fb1422的网卡
/ # ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue qlen 1
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
26952: eth0@if26953: <BROADCAST,MULTICAST,UP,LOWER_UP,M-DOWN> mtu 1500 qdisc noqueue
    link/ether 02:42:c0:a8:00:03 brd ff:ff:ff:ff:ff:ff
    inet 192.168.0.3/24 brd 192.168.0.255 scope global eth0
       valid_lft forever preferred_lft forever
26960: eth1@if26961: <BROADCAST,MULTICAST,UP,LOWER_UP,M-DOWN> mtu 1500 qdisc noqueue
    link/ether 02:42:ac:12:00:03 brd ff:ff:ff:ff:ff:ff
    inet 172.18.0.3/16 brd 172.18.255.255 scope global eth1
       valid_lft forever preferred_lft forever      
       
#在172.18.0.2这个容器 ping 172.18.0.3可以ping通
#但是ping 192.168.0.3，发现ping不通，但是可以ping通他的网关
/ # ping 192.168.0.1
PING 192.168.0.1 (192.168.0.1): 56 data bytes
64 bytes from 192.168.0.1: seq=0 ttl=64 time=0.095 ms
64 bytes from 192.168.0.1: seq=1 ttl=64 time=0.092 ms
64 bytes from 192.168.0.1: seq=2 ttl=64 time=0.100 ms
^C
--- 192.168.0.1 ping statistics ---
3 packets transmitted, 3 packets received, 0% packet loss
round-trip min/avg/max = 0.092/0.095/0.100 ms
/ # ping 192.168.0.3
PING 192.168.0.3 (192.168.0.3): 56 data bytes
^C
--- 192.168.0.3 ping statistics ---
3 packets transmitted, 0 packets received, 100% packet loss
/ # ping 172.18.0.3
PING 172.18.0.3 (172.18.0.3): 56 data bytes
64 bytes from 172.18.0.3: seq=0 ttl=64 time=0.236 ms
64 bytes from 172.18.0.3: seq=1 ttl=64 time=0.100 ms
64 bytes from 172.18.0.3: seq=2 ttl=64 time=0.087 ms
^C
--- 172.18.0.3 ping statistics ---
3 packets transmitted, 3 packets received, 0% packet loss

```

![image-20220519222647469](C:\Users\shunyu\AppData\Roaming\Typora\typora-user-images\image-20220519222647469.png)

## 容器间通信

容器间可以通过IP docker DNS Server或者joined容器三种通信方式通信

### IP 通信

容器间通信必须要有属于同一个网络的网卡，这个是容器通信的必要条件

- 创建容器时通过 --network指定网络，通过 --ip指定ip地址
- 通过docker network connect net_name container_name 将现有容器加入到指定网络

### Docker DNS Server

docker daemon内嵌了一个DNS Server，使容器可以之间通过容器名通信

在容器启动时，使用--name指定容器名就可以了

```
root@ubuntu:~# docker run -it --network=my_net_1 --name=name1 busybox
/ # ping name2
PING name2 (192.168.0.3): 56 data bytes
64 bytes from 192.168.0.3: seq=0 ttl=64 time=0.085 ms

root@ubuntu:~# docker run -it --network=my_net_1 --name=name2 busybox
/ # ping name1
PING name1 (192.168.0.2): 56 data bytes
64 bytes from 192.168.0.2: seq=0 ttl=64 time=0.187 ms
64 bytes from 192.168.0.2: seq=1 ttl=64 time=0.083 ms
```

如果两个容器所指定的不是同一个网络，则无法通信，使用docker network connect 将name1的容器加入到my_net之后才可以通信

```
root@ubuntu:~# docker run -it --network=my_net --name=name3 busybox
/ # ping name1
ping: bad address 'name1'

#使用docker network connect my_net name1

/ # ping name1
PING name1 (172.18.0.3): 56 data bytes
64 bytes from 172.18.0.3: seq=0 ttl=64 time=0.190 ms
64 bytes from 172.18.0.3: seq=1 ttl=64 time=0.110 ms
```

默认的bridge网络无法使用dns

### joined网络

joined使两个或者多个容器共享一个网络栈，共享网卡和配置信息

使用 --name=container:name1 指定和名称为name1的容器共享网卡

```
root@ubuntu:~# docker run -d --name=web httpd
7add8ef6bcbcacdf8bd924ef3be9b109ca11194bb9f8d948cdb90e9c733e181a

root@ubuntu:~# docker run -it --network=container:web busybox
/ # ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue qlen 1
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
26976: eth0@if26977: <BROADCAST,MULTICAST,UP,LOWER_UP,M-DOWN> mtu 1500 qdisc noqueue
    link/ether 02:42:ac:11:00:03 brd ff:ff:ff:ff:ff:ff
    inet 172.17.0.3/16 brd 172.17.255.255 scope global eth0
       valid_lft forever preferred_lft forever

# 查看httpd容器的网卡信息
docker inspect web
....
"Gateway": "172.17.0.1",
            "GlobalIPv6Address": "",
            "GlobalIPv6PrefixLen": 0,
            "IPAddress": "172.17.0.3",
            "IPPrefixLen": 16,
            "IPv6Gateway": "",
            "MacAddress": "02:42:ac:11:00:03",
.....
```

joined容器使用以下场景

- 不同容器中的程序希望通过lookback高效快速的通信
- 希望监控其他容器的网络流量

## 将容器与外部世界连接

### 容器访问外部世界

**通过NAT，docker实现了容器对外网的访问**

容器默认可以访问host主机可以访问的任何网络

```
root@ubuntu:~# iptables -t nat -S
-P PREROUTING ACCEPT
-P INPUT ACCEPT
-P OUTPUT ACCEPT
-P POSTROUTING ACCEPT
-N DOCKER
-A PREROUTING -m addrtype --dst-type LOCAL -j DOCKER
-A OUTPUT ! -d 127.0.0.0/8 -m addrtype --dst-type LOCAL -j DOCKER
-A POSTROUTING -s 192.168.0.0/24 ! -o br-30fb2111e320 -j MASQUERADE
-A POSTROUTING -s 172.18.0.0/16 ! -o br-232d3cfcfdcb -j MASQUERADE
-A POSTROUTING -s 172.17.0.0/16 ! -o docker0 -j MASQUERADE
#如果网桥docker0收到来自 172.17.0.0/16 网段的外出包， 把它交给MASQUERADE处理，将包的源地址替换成host的地址发出
```

在容器中ping百度，并通过tcpdump进行抓包分析

```
#从docker0网卡出去的包
root@ubuntu:~# tcpdump -i docker0 -n icmp
tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
listening on docker0, link-type EN10MB (Ethernet), capture size 262144 bytes
23:16:10.256458 IP 172.17.0.5 > 180.101.49.12: ICMP echo request, id 9, seq 0, length 64
23:16:10.270200 IP 180.101.49.12 > 172.17.0.5: ICMP echo reply, id 9, seq 0, length 64

#从ens160网卡出去的包
root@ubuntu:~# tcpdump -i ens160 -n icmp
tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
listening on ens160, link-type EN10MB (Ethernet), capture size 262144 bytes
23:17:27.488164 IP 10.182.79.36 > 180.101.49.12: ICMP echo request, id 10, seq 0, length 64
23:17:27.540554 IP 180.101.49.12 > 10.182.79.36: ICMP echo reply, id 10, seq 0, length 64
```

![image-20220519232037671](C:\Users\shunyu\AppData\Roaming\Typora\typora-user-images\image-20220519232037671.png)

### 外部世界访问容器

**通过端口映射让外网访问到容器**

docker可将容器对外提供服务的端口映射到host的某个端口，外网通过该端口访问容器，容器启动时通过-p参数映射端口

- -p 33392:9200 将容器的9200端口映射到host 主机的33392端口  静态映射
- -p 80 将80端口映射到host主机的随机一个端口  动态映射

```
root@ubuntu:~# docker ps -a
CONTAINER ID   IMAGE        COMMAND                  CREATED       STATUS       PORTS                                                                                                                                            NAMES
1419b9c64c48   elk          "/bin -c ../run.sh"   9 days ago    Up 9 days    0.0.0.0:5601->5601/tcp, :::5601->5601/tcp, 514/tcp, 9300/tcp, 0.0.0.0:9200->9200/tcp, :::9200->9200/tcp, 0.0.0.0:515->514/udp, :::515->514/udp   elk
d4156c3dc564   registry:2   "/entrypoint.sh /etc…"   7 weeks ago   Up 13 days   0.0.0.0:5000->5000/tcp, :::5000->5000/tcp

root@ubuntu:~# curl 10.182.79.36:9200
{
  "name" : "node-1",
  "cluster_name" : "elasticsearch",
  "cluster_uuid" : "TsGXocEsR4aRFj6OFWZrww",
  "version" : {
    "number" : "7.6.1",
    "build_flavor" : "default",
    "build_type" : "tar",
    "build_hash" : "aa751e09be0a5072e8570670309b1f12348f023b",
    "build_date" : "2020-02-29T00:15:25.529771Z",
    "build_snapshot" : false,
    "lucene_version" : "8.4.0",
    "minimum_wire_compatibility_version" : "6.8.0",
    "minimum_index_compatibility_version" : "6.0.0-beta1"
  },
  "tagline" : "You Know, for Search"
}
```

![image-20220519233518638](C:\Users\shunyu\AppData\Roaming\Typora\typora-user-images\image-20220519233518638.png)

