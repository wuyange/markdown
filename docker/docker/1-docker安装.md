# docker的安装和卸载

## centos

### 通过脚本安装

安装脚本

```shell
#!/bin/bash
# 移除掉旧的版本
sudo yum remove docker \
                  docker-client \
                  docker-client-latest \
                  docker-common \
                  docker-latest \
                  docker-latest-logrotate \
                  docker-logrotate \
                  docker-selinux \
                  docker-engine-selinux \
                  docker-engine

# 删除所有旧的数据
sudo rm -rf /var/lib/docker

#  安装依赖包
sudo yum install -y yum-utils \
  device-mapper-persistent-data \
  lvm2

# 添加源，使用了阿里云镜像
sudo yum-config-manager \
    --add-repo \
    http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo

# 配置缓存
sudo yum makecache fast

# 安装最新稳定版本的docker
sudo yum install -y docker-ce

# 配置镜像加速器
sudo mkdir -p /etc/docker
sudo tee /etc/docker/daemon.json <<-'EOF'
{
  "registry-mirrors": ["http://hub-mirror.c.163.com"]
}
EOF

# 启动docker引擎并设置开机启动
sudo systemctl start docker
sudo systemctl enable docker

# 配置当前用户对docker的执行权限
sudo groupadd docker
sudo gpasswd -a ${USER} docker
sudo systemctl restart docker
```

### 手动安装

```shell
#安装依赖包，yum-utils提供yum-config-manager工具，devicemapper存储驱动需要device-mapper-persistent-data和lvm2
sudo yum install -y yum-utils \
  device-mapper-persistent-data \
  lvm2
#使用下面的命令安装稳定版仓库，即使安装最新体验版或者是测试版也需要稳定版仓库。
sudo yum-config-manager \
    --add-repo \
    https://download.docker.com/linux/centos/docker-ce.repo
#安装最新版本的docker CE
sudo yum install -y docker-ce
#安装指定版本的docker CE
yum install -y docker-ce-18.03.0.ce
#启动docker CE
sudo systemctl start docker
```

### 卸载

#### 方式一

```shell
sudo yum remove docker \
                  docker-client \
                  docker-client-latest \
                  docker-common \
                  docker-latest \
                  docker-latest-logrotate \
                  docker-logrotate \
                  docker-selinux \
                  docker-engine-selinux \
                  docker-engine
```

#### 方式二

```shell
杀死docker有关的容器：
docker kill $(docker ps -a -q)
删除所有docker容器：
docker rm $(docker ps -a -q)
删除所有docker镜像：
docker rmi $(docker images -q)
停止 docker 服务：
systemctl stop docker
删除docker相关存储目录：
rm -rf /etc/docker
rm -rf /run/docker
rm -rf /var/lib/dockershim
rm -rf /var/lib/docker
如果删除不掉，则先umount：
umount /var/lib/docker/devicemapper
然后再重新执行上面那步“删除docker相关存储目录”。
经过上面一系列准备后，我们终于到了最后环节，开始删除docker。
查看系统已经安装了哪些docker包：
[root@localhost ~]# yum list installed | grep docker
containerd.io.x86_64                 1.2.13-3.2.el7                 @docker-ce-stable
docker-ce.x86_64                     3:19.03.12-3.el7               @docker-ce-stable
docker-ce-cli.x86_64                 1:19.03.12-3.el7               @docker-ce-stable
卸载相关包：
[root@localhost ~]# yum remove containerd.io.x86_64 docker-ce.x86_64 docker-ce-cli.x86_64
```

## ubuntu

### 手动安装

```shell
#升级apt包索引
sudo apt-get update
#安装能够让apt使用HTTPS的包
sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common
#添加官方的GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
#设置稳定版源
sudo add-apt-repository \
   "deb [arch=arm64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
#安装最新版本的docker CE
sudo apt-get install docker-ce
```

### 卸载

```shell
#删除某软件及其安装时自动安装的所有包，命令如：
sudo apt-get autoremove docker docker-ce docker-engine docker.io containerd runc
#删除docker卸载残留，命令如：
dpkg -l | grep dockerdpkg -l |grep ^rc|awk '{print $2}' |sudo xargs dpkg -P # 删除无用的相关的配置文件
#卸载没有删除的docker相关插件，命令如：
sudo apt-get autoremove docker-ce-*
#删除docker的相关配置，命令如：
sudo rm -rf /etc/systemd/system/docker.service.dsudo rm -rf /var/lib/docker
#检查是否卸载成功。
docker --version
```

