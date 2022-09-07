# docker容器

## 让容器长时间运行

容器的生命周期依赖于启动时执行的命令，只要命令不结束，容器也就不会退出

![image-20220421191620727](C:\Users\shunyu\AppData\Roaming\Typora\typora-user-images\image-20220421191620727.png)

![image-20220421213729533](C:\Users\shunyu\AppData\Roaming\Typora\typora-user-images\image-20220421213729533.png)

```html
docker run --name xxx -d imagesName
--name 指定容器的名称
-d 让容器再后台运行，并返回容器的长ID， 我们可以通过容器的长ID、短ID或者容器的名称来操作容器
```

## 进入容器的方法

### docker attach

```
#可以通过docker attach，进入到容器启动命令的终端
root@ubuntu:~# docker run --name my_ubuntu_1  -d ubuntu /bin/bash -c "while true ;do sleep 1;echo hhhh; done"
644b80c564b793418e48bca1d03dd73b4c3dc0aeba269d3362a83a2d569651ef
root@ubuntu:~# docker attach 644b80c564b793418e48bca1d03dd73b4c3dc0aeba269d3362a83a2d569651ef
hhhh
hhhh
```

### docker exec

```
#可以通过docker exec 进入到相同的容器
root@ubuntu:~# docker run --name my_ubuntu_1  -d ubuntu /bin/bash -c "while true ;do sleep 1;echo hhhh; done"
afc8eaaf59c5dbec30cfbb3bd26ae9fd16fa18148798ffa88fd22eac05e5412b
root@ubuntu:~# docker exec -it my_ubuntu_1 bash
root@afc8eaaf59c5:/#

-it 以交互模式打开
bash  进入到容器中之后执行bash

#如果exec后面接的命令不是长时间运行的命令，也会执行完就退出
root@ubuntu:~# docker exec -it my_ubuntu_1 pwd
/
root@ubuntu:~#

#执行exit就会退出这个终端
```

### attach 和 exec的区别

- attach直接进入容器启动命令的终端，不会启动新的进程
- exec 则是在容器中打开新的终端，并且可以启动新的进程
- attach退出后容器就也退出了，但是exec退出了容器还是在后台执行

```
#先运行一个容器
root@ubuntu:~# docker run --name my_ubuntu_1  -it  ubuntu
root@b534d5f6f93f:/# ps aux
USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root         1  0.3  0.0   4108  3400 pts/0    Ss   03:11   0:00 bash
root         9  0.0  0.0   5892  2888 pts/0    R+   03:11   0:00 ps aux
#在另一个终端2通过exec来进入容器
root@ubuntu:~# docker exec -it my_ubuntu_1 bash
root@b534d5f6f93f:/#
#回到之前的终端1，查看进程，有新的进程
root@b534d5f6f93f:/# ps aux
USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root         1  0.0  0.0   4108  3508 pts/0    Ss   03:11   0:00 bash
root        10  0.2  0.0   4108  3500 pts/1    Ss+  03:11   0:00 bash
root        18  0.0  0.0   5892  2896 pts/0    R+   03:11   0:00 ps aux
#在另一个终端2，先退出exec，然后使用attach连接容器
root@ubuntu:~# docker attach my_ubuntu_1
root@b534d5f6f93f:/#
#回到之前的终端1查看进程，发现没有新的进程
root@b534d5f6f93f:/# ps aux
USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root         1  0.0  0.0   4108  3508 pts/0    Ss   03:11   0:00 bash
root        19  0.0  0.0   5892  2912 pts/0    R+   03:14   0:00 ps aux
#回到终端2，发现之前在终端1中执行的命令也在终端2中显示
root@ubuntu:~# docker attach my_ubuntu_1
root@b534d5f6f93f:/# ps aux
USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root         1  0.0  0.0   4108  3508 pts/0    Ss   03:11   0:00 bash
root        19  0.0  0.0   5892  2912 pts/0    R+   03:14   0:00 ps aux
root@b534d5f6f93f:/#
#使用exit退出attach连接，并使用docker ps -a查看，发现my_ubuntu_1的状态为退出
```

## stop/start/restart/pause/unpause/rm

```
docker stop 容器名       停止容器
docker start 容器名      开启容器   会保留容器第一次启动时的参数
docker restart 容器名    重启容器
可以在运行容器时，设置 --restart自动重启
--restart=always  无论容器因为什么原因退出，都立即重启
--restart=on-failure:3  除了容器正常退出外，都会重启，最多重启3次，正常退出的容器代码为0

docker pause 容器名     暂停容器 暂停时不会占用资源
docker unpause 容器名   取消暂停

docker rm 容器名        删除容器 只能删除已经退出的容器
docker rm -v $(docker ps -aq -f status=exited) 删除所有的已经退出的容器
```

## docker各种状态

![image-20220504233712973](C:\Users\shunyu\AppData\Roaming\Typora\typora-user-images\image-20220504233712973.png)

- `docker create` 命令是创建容器
- `docker run`命令是`docker create `和`docker start`命令的组合
- 除非通过`docker stop`或者`docker kill`退出容器，否则`--restart`参数都会生效

## 资源限制

### 内存限额

- `-m`或者`--memory`：设置物理内存的使用限额
- `--memory-swap`：设置内存和swap两个部分的设用限额
- 默认情况下上面两组为-1，表示对容器的内存和swap没有限制
- 如果只指定`-m`参数，不指定`--memory-swap`，那么`--memory-swap`默认为`-m`的两倍

```
docker run -m 200m --memory-swap=300m ubuntu
#设置该容器最多使用200mb的内存和100mb的swap

docker run -it -m 200m --memory-swap=300m progrium/stress --vm 1 --vm-bytes 280m
#--vm 1:表示启动一个线程
#--vm-bytes 280m:表示每个线程使用280mb内存

#如果工作线程分配超出--memory-swap设置的值，则线程报错，容器退出
root@ubuntu:~# docker run -it -m 200M --memory-swap=250m progrium/stress --vm 1 --vm-bytes 280M
stress: info: [1] dispatching hogs: 0 cpu, 0 io, 1 vm, 0 hdd
stress: dbug: [1] using backoff sleep of 3000us
stress: dbug: [1] --> hogvm worker 1 [8] forked
stress: dbug: [8] allocating 293601280 bytes ...
stress: dbug: [8] touching bytes in strides of 4096 bytes ...
stress: FAIL: [1] (416) <-- worker 8 got signal 9
stress: WARN: [1] (418) now reaping child worker processes
stress: FAIL: [1] (422) kill error: No such process
stress: FAIL: [1] (452) failed run completed in 1s

```

>ubuntu使用`--memory-swap`参数参数时会报错
>
>```
>WARNING: Your kernel does not support swap limit capabilities or the cgroup is not mounted. Memory limited without swap.
>```
>
>解决方案
>
>- 修改系统的/etc/default/grub file文件。使用vim在这个文件中添加一行：
>  ```
>  GRUB_CMDLINE_LINUX="cgroup_enable=memory swapaccount=1"
>  ```
>
>- 更新系统的GRUB：
>  ```
>  sudo update-grub
>  ```
>
>- `reboot`后生效

## CPU限额

- 默认设置下，所有的容器平等的使用host主机的CPU资源，并且没有限制
- `-c`或者`--cpu-shares`设置容器使用CPU的权重，不指定时的默认值为1024，权重是一个相对的权重值，最终能分配到的CPU资源取决于他的`cpu share`占所有容器的`cpu share`的总和的比列
- 按权重分配CPU只会发生在CPU资源紧张的情况下

```
root@ubuntu:~# docker run --name x1 -dit -c 512 progrium/stress --cpu 8
fdf6abcae1ef8ccddee66dd326b775f491c75be14830997056aedfe263c8534e
root@ubuntu:~# docker run --name x2 -dit -c 1024 progrium/stress --cpu 8
b1cdc4d058468528a9bb18d32bc4a7ac95be28a1bfdf0b0a1cf0be0cadf72edc
root@ubuntu:~# top
top - 19:44:15 up 28 min,  3 users,  load average: 8.43, 4.52, 1.93
Tasks: 367 total,  17 running, 350 sleeping,   0 stopped,   0 zombie
%Cpu(s): 99.9 us,  0.1 sy,  0.0 ni,  0.0 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st
KiB Mem :  4045536 total,  1873756 free,  1165552 used,  1006228 buff/cache
KiB Swap:  4189692 total,  4189692 free,        0 used.  2572004 avail Mem

  PID USER      PR  NI    VIRT    RES    SHR S  %CPU %MEM     TIME+ COMMAND
23908 root      20   0    7312    100      0 R  66.8  0.0   0:10.09 stress
23909 root      20   0    7312    100      0 R  66.8  0.0   0:10.07 stress
23913 root      20   0    7312    100      0 R  66.8  0.0   0:10.14 stress
23914 root      20   0    7312    100      0 R  66.8  0.0   0:10.06 stress
23915 root      20   0    7312    100      0 R  66.8  0.0   0:10.06 stress
23907 root      20   0    7312    100      0 R  66.4  0.0   0:10.06 stress
23911 root      20   0    7312    100      0 R  66.4  0.0   0:10.26 stress
23912 root      20   0    7312    100      0 R  66.4  0.0   0:09.98 stress
23649 root      20   0    7312     96      0 R  33.2  0.0   0:16.19 stress
23651 root      20   0    7312     96      0 R  33.2  0.0   0:16.16 stress
23652 root      20   0    7312     96      0 R  33.2  0.0   0:16.09 stress
23653 root      20   0    7312     96      0 R  33.2  0.0   0:16.34 stress
23655 root      20   0    7312     96      0 R  33.2  0.0   0:16.27 stress
23648 root      20   0    7312     96      0 R  32.9  0.0   0:16.24 stress
23650 root      20   0    7312     96      0 R  32.9  0.0   0:15.91 stress
23654 root      20   0    7312     96      0 R  32.9  0.0   0:16.31 stress
```

## Block IO带宽限额

- `block IO`权重：设置`--blkio-weight`参数来改变容器的`block IO`的优先级
  - `--blkio-weight`设置的也是相对权重值，默认为500
- `bps`和`iops`: `bps`是每秒读写的数量 `iops`是每秒IO的次数
  - `device-read-bps`:限制读某个设备的bps
  - `device-write-bps`:限制写某个设备的bps
  - `device-read-iops`:限制读某个设备的iops
  - `device-write-iops`:限制写某个设备的iops

## 实现容器的底层技术

### cgroup

- 设置进程的CPU、内存和IO资源的限额
- `/sys/fs/cgroup/cpu/docker`:存放容器的cpu配置
- `/sys/fs/cgroup/memory/docker`:存放容器的内存配置
- `/sys/fs/cgroup/blkio/docker`:存放容器的Block IO带宽限额

```
root@ubuntu:~# docker run --name x2 -d -c 1024 progrium/stress --cpu 1
d2be5e5627d02a337c5a56425061cad5f586abcf7fbc05b22540f08f872dd103
root@ubuntu:~# cat /sys/fs/cgroup/cpu/docker/d2be5e5627d02a337c5a56425061cad5f586abcf7fbc05b22540f08f872dd103/cpu.shares
1024
```

### namespace

- `namespace`实现了容器间资源的隔离
- `Linux`使用了6种`namespace`，分布对应6种资源：`Mount、UTS、IPC、Network、PID和User`
  - `Mount namespace`:让容器看上去拥有整个文件系统
  - `UTS namespace`:让容器有自己的hostname
    - 默认情况下容器的`hostname`是他的短ID
    - 可以通过`docker run -h myhostname -it ubuntu`设置
  - `IPC namespace`:让容器拥有自己的共享内存和信号量来实现进程间的通信
  - `PID namespace`:让容器拥有自己独立的一套PID
  - `network namespace`:让容器用于自己的独立网卡、IP、路由等
  - `user namespace`:让容器能够管理自己的用户

## elk dockerfile

```
from ubuntu:16.04
ENV TZ=Asia/Shanghai
# 开放端口
expose 9200
expose 5601
expose 9300
expose 514
# 安装jdk
run apt-get update && apt-get install openjdk-8-jdk -y
# 下载安装包
run mkdir /home/elk
run useradd -d /home/elk elk
workdir /home/elk
add elk.tar.gz /home/elk
add run.sh /home/elk
run chown -R elk:elk /home/elk
workdir /home/elk/elk
user elk
cmd elk/run.sh


run apt-get update && yum install -y java-1.8.0-openjdk-devel.x86_64   

run.sh
elasticsearch-7.6.1/bin/elasticsearch &
kibana-7.6.1-darwin-x86_64/bin/kibana &
```

## elk官方镜像

### ElasticSearch

- 第一步：拉取镜像

```sh
docker pull docker.elastic.co/elasticsearch/elasticsearch:6.3.2
```

- 第二步：安装

```sh
docker run -d --name es -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:6.3.2
```

- 第三步：配置跨域

```sh
docker exec -it es /bin/bash
# 修改 elasticsearch.yml
vi config/elasticsearch.yml
# 加入跨域配置
http.cors.enabled: true
http.cors.allow-origin: "*"
```

- 第四步：重启容器

```sh
docker restart es 
```

### ElasticSearch-Head

通过`ElasticSearch-Head`，查看`ElasticSearch`相关信息

- 第一步：拉取

```sh
docker pull mobz/elasticsearch-head:5
```

- 第二步：安装

```sh
docker run -d --name es_admin -p 9100:9100 mobz/elasticsearch-head:5
```

### 安装logstash

- 第一步：安装

```shell
docker run --name es_logstash -d docker.elastic.co/logstash/logstash:6.2.4
```

- 第二步：修改logstash.yml文件

进入容器：

```sh
# 进入容器
docker exec -it es_logstash /bin/bash
# 修改配置文件
vi config/logstash.yml
# 修改为以下内容
http.host: "0.0.0.0"
xpack.monitoring.elasticsearch.url: http://10.182.79.36:9200
xpack.monitoring.elasticsearch.username: shunyu
xpack.monitoring.elasticsearch.password: hillstone
```

### 安装kibana

- 第一步：拉取

```sh
docker pull docker.elastic.co/kibana/kibana:6.3.2
```

- 第二步：安装

```sh
docker run --name es_kibana -p 5601:5601 -d -e ELASTICSEARCH_URL=http://10.182.79.36:9200 docker.elastic.co/kibana/kibana:6.3.2
```

- 第三步：修改

```sh
# 进入容器
docker exec -it es_logstash /bin/bash
# 修改pipeline下的logstash.conf文件
vi pipeline/logstash.conf
# 修改的内容为
input {
        file {
            codec=> json
                path => "/usr/local/*.json"
        }
}
filter {
  #定义数据的格式
  grok {
    match => { "message" => "%{DATA:timestamp}\|%{IP:serverIp}\|%{IP:clientIp}\|%{DATA:logSource}\|%{DATA:userId}\|%{DATA:reqUrl}\|%{DATA:reqUri}\|%{DATA:refer}\|%{DATA:device}\|%{DATA:textDuring}\|%{DATA:duringTime:int}\|\|"}
  }
}
output {
   elasticsearch{
     hosts=> "http://10.182.79.36:9200"
   }
}
```

- 容器全部重启

```sh
docker restart 122bddb80fb9
docker restart es_admin
docker restart 8a4cba6ae3aa
docker restart 415d5e4b3383
```

```
input{
    syslog{port => '514'}
}
filter {
  if [message] =~"«Í«Í" {
    ruby {
      code => "event.set('message',(event.get('message') + 'FFFF').encode('ISO-8859-1'))"
      add_field => {"category" => "binary"}
      remove_field => ['facility_label','severity_label','@version','facility','severity','tags','tamp','priority']
    }
  } else {
  ruby {
    code => "
    event.set('message',(event.get('message') + 'FFFF').encode('ISO-8859-1').force_encoding('UTF-8
    event.set('timestamp_utc',Time.now.utc.iso8601)"
  }
  mutate {
    remove_field => ['@version']
    remove_field => ['@timestamp']
    remove_field => ['timestamp']
    remove_field => ['severity_label']
    remove_field => ['severity']
    remove_field => ['facility_label']
    remove_field => ['facility']
    rename => ['logsource','hostname']
    rename => ['program','appname']
  }
}
}
output{
    elasticsearch{
         hosts => "http://10.182.79.36:9200"
         user => es
         password => hillstone
         codec => "rubydebug"
         index => "yushun-%{+YYYY-MM-dd}"
    }
}
```

作业

- 下载`elasticsearch` `kibana` `logstash`安装包，并修改其中的配置文件

```
#elasticsearch.yml 添加下面几项
node.name: node-1
network.host: 0.0.0.0
http.port: 9200
cluster.initial_master_nodes: ["node-1"]

#jvm.options 修改下面几项
8-13:-XX:+UseConcMarkSweepGC  修改为  8-13:-XX:+UseG1GC

#kibana.yml 添加下面几项
server.port: 5601
server.host: "0.0.0.0"
elasticsearch.hosts: ["http://localhost:9200"]

#logstash-7.6.1/config中添加文件log_syslog
input{
    syslog{
    type => "system-syslog"
    port => "514"
    }
}
output{
    elasticsearch{
         hosts => "http://10.182.79.36:9200"
         user => es
         password => hillstone
         codec => "rubydebug"
         index => "yushun-%{+YYYY-MM-dd}"
    }
}
```

- 压缩安装包，并移动到dockerfile所在目录

```
tar -zcvf elk.tar.gz elk
mv elk.tar.gz  dockerfile所在目录
```

- 进入到dockerfile所在目录，并创建镜像

```
docker build -t elk . -f ./dockerfile

#dockerfile
from centos:7
ENV TZ=Asia/Shanghai
# 开放端口
expose 9200
expose 5601
expose 9300
expose 514
# 安装jdk
run yum update -y  && yum install -y java-1.8.0-openjdk-devel.x86_64
run mkdir /home/elk
run useradd -d /home/elk elk
workdir /home/elk
add elk.tar.gz /home/elk
add run.sh /home/elk
run chmod +x /home/elk/run.sh
run chown -R elk:elk /home/elk
workdir /home/elk/elk
cmd ../run.sh

#run.sh
su elk -c "nohup elasticsearch-7.6.1/bin/elasticsearch &"
su elk -c "nohup kibana-7.6.1-linux-x86_64/bin/kibana &"
nohup logstash-7.6.1/bin/logstash -f logstash-7.6.1/config/log_syslog
```

- 启动容器

```
docker run --name elk -d -p 9200:9200 -p 5601:5601 -p 515:514/udp  elk
```



