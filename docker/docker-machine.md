# docker-machine

对于多主机环境手工安装`docker`效率低，而且不容易保证一致性，针对这个问题，`docker`给出了一个解决方案就是`docker Machine`

## 安装docker machine

```shell
# linux命令
base=https://github.com/docker/machine/releases/download/v0.16.0 &&
  curl -L $base/docker-machine-$(uname -s)-$(uname -m) >/tmp/docker-machine &&
  sudo mv /tmp/docker-machine /usr/local/bin/docker-machine &&
  chmod +x /usr/local/bin/docker-machine
  
# 方法二
去网上找安装包，改名为docker-machine，下载后发送到/usr/local/bin，并使用chmod +x 
```

## 创建Machine

- 创建`docker machine`时，要求能无密码登录远程主机，所以需要将`ssh key`复制到主机

```shell
# 在docker machine主机上使用以下命令
# 先使用ssh-keygen生成ssh公钥，然后一路回车
# ssh-copy-id  root@远程主机的ip，然后根据提示输入yes 和 远程主机的密码
root@ubuntu:/usr/local/bin# ssh-copy-id -i ~/.ssh/id_rsa.pub root@10.182.244.94
/usr/bin/ssh-copy-id: INFO: Source of key(s) to be installed: "/root/.ssh/id_rsa.pub"
The authenticity of host '10.182.244.94 (10.182.244.94)' can't be established.
ECDSA key fingerprint is SHA256:2NzzCMHrJdlxsrZvDQQWyZyonSDa38cwajdsTcVGXt8.
Are you sure you want to continue connecting (yes/no)? yes
/usr/bin/ssh-copy-id: INFO: attempting to log in with the new key(s), to filter out any that are already installed
/usr/bin/ssh-copy-id: INFO: 1 key(s) remain to be installed -- if you are prompted now it is to install the new keys
root@10.182.244.94's password:

Number of key(s) added: 1

Now try logging into the machine, with:   "ssh 'root@10.182.244.94'"
and check to make sure that only the key(s) you wanted were added.
```

- 执行`docker-machine create` 创建机器

```shell
# docker-machine create --driver generic --generic-ip-address=10.182.244.94 host1
# --driver generic 指定使用generic来部署docker
# --generic-ip-address 指定目标系统的IP，并命名为host1
root@ubuntu:/usr/local/bin# docker-machine create --driver generic --generic-ip-address=10.182.244.94 host1
Creating CA: /root/.docker/machine/certs/ca.pem
Creating client certificate: /root/.docker/machine/certs/cert.pem
Running pre-create checks...
Creating machine...
(host1) No SSH key specified. Assuming an existing key at the default location.
Waiting for machine to be running, this may take a few minutes...
Detecting operating system of created instance...
Waiting for SSH to be available...
Detecting the provisioner...
Provisioning with ubuntu(systemd)...
```

- 执行`docker-machine ls`查看控制的机器

```shell
[root@centos7 ~]# docker-machine ls
NAME    ACTIVE   DRIVER    STATE     URL                        SWARM   DOCKER      ERRORS
host1   -        generic   Running   tcp://10.182.244.94:2376           v20.10.17
```

- 在`host1`查看`docker daemon`的具体配置`cat /etc/systemd/system/docker.service.d/10-machine.conf`

```shell
root@host2:/etc/systemd/system/docker.service.d# cat /etc/systemd/system/docker.service.d/10-machine.conf
[Service]
ExecStart=
ExecStart=/usr/bin/dockerd -H tcp://0.0.0.0:2376 -H unix:///var/run/docker.sock --storage-driver overlay2 --tlsverify --tlscacert /etc/docker/ca.pem --tlscert /etc/docker/server.pem --tlskey /etc/docker/server-key.pem --label provider=generic
Environment=
# -H tcp://0.0.0.0:2376: 使docker daemon接受远程连接
# --tls*:对远程连接启用安全认证和加密
# 并且此时主机的hostname已经被设置为host1
```

## 管理machine

执行远程`docker`命令需要通过`-H`指定目标主机的连接字符串

```shell
[root@centos7 ~]# docker -H tcp://10.182.79.36 ps -a
CONTAINER ID   IMAGE     COMMAND                  CREATED       STATUS                        PORTS                                                                                                                                            NAMES
b4bb3eb6afdf   httpd     "httpd-foreground"       3 weeks ago   Exited (0) 25 minutes ago                                                                                   
```

通过`docker machine`可以让这个过程更简单，`docker-machine env host1`显示访问`host1`需要的所有环境变量

```shell
[root@centos7 ~]# docker-machine env host1
export DOCKER_TLS_VERIFY="1"
export DOCKER_HOST="tcp://10.182.244.94:2376"
export DOCKER_CERT_PATH="/root/.docker/machine/machines/host1"
export DOCKER_MACHINE_NAME="host1"
# Run this command to configure your shell:
# eval $(docker-machine env host1)

# 执行eval $(docker-machine env host1)可以切换到host1，在此状态下执行的所有docker命令的效果都相当于在host1上执行
[root@centos7 bash_completion.d]# eval $(docker-machine env host1)
[root@centos7 bash_completion.d [host1]]# docker ps -a
CONTAINER ID   IMAGE     COMMAND              CREATED         STATUS         PORTS     NAMES
0e98671bc1a9   httpd     "httpd-foreground"   6 minutes ago   Up 6 minutes   80/tcp    host1Httpd
0df02bbc47e9   httpd     "httpd-foreground"   7 minutes ago   Created 

# 可以通过eval $(docker-machine env host2)切换到host2上
# docker-machine upgrade:更新machine的docker到最新版本，可批量执行
dockers-machine upgrade host1
```

