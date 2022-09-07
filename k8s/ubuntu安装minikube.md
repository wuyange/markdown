# ubuntu安装minikube

参考链接： https://zhuanlan.zhihu.com/p/429690423

## 安装docker

1. 如果之前有安装过`docker`，可以先卸载：

```shell
apt-get remove docker docker-engine docker.io
```

2. 更新apt安装包索引

```shell
apt-get update
```

3. 安装软件包以允许`apt`通过`HTTPS`

```shell
sudo apt-get install apt-transport-https ca-certificates curl software-properties-commo
```

4. 添加`Docker`官方的`GPG`密钥

```shell
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
```

5. 安装稳定版仓库

```shell
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
```

6. 安装`docker`

```shell
apt-get install docker.io
```

7. 启动`docker`服务

```shell
systemctl start docker
```

8. 通过修改`daemon`配置加速

```shell
$ cd /etc/docker
# 在daemon.json文件末尾追加如下配置：
$ sudo tee /etc/docker/daemon.json <<-'EOF'
{
  "registry-mirrors": ["https://dhx52mku.mirror.aliyuncs.com"]
}
EOF

# 重启docker
$ sudo systemctl daemon-reload
$ sudo systemctl restart docker
```

## 安装minikube

1. 直接安装`minikube`

```shell
curl -Lo minikube https://kubernetes.oss-cn-hangzhou.aliyuncs.com/minikube/releases/v1.23.1/minikube-linux-amd64 && chmod +x minikube && sudo mv minikube /usr/local/bin/
```

2. 启动`minikube`

```shell
minikube start

# 执行minikube start出现 The "docker" driver should not be used with root privileges 的报错，直接执行以下命令，强制使用docker

minikube start --force --driver=docker

# 如果提示 '! The image 'registry.cn-hangzhou.aliyuncs.com/google_containers/coredns/coredns:v1.8.4' was not found; unable to add it to cache.' 执行下列命令，并重新执行minikube start --force --driver=docker

docker pull registry.cn-hangzhou.aliyuncs.com/google_containers/coredns:1.8.4
docker tag registry.cn-hangzhou.aliyuncs.com/google_containers/coredns:1.8.4 registry.cn-hangzhou.aliyuncs.com/google_containers/coredns/coredns:v1.8.4
```

3. 让minikube下载kubectl客户端命令工具

```shell
minikube kubectl -- get pods -A
```

4. 开启控制台

```shell
minikube dashboard
```

5. 此时的`minikube kubectl --`就相当于k8s里的`kubectl`命令，我们可以通过起别名的方式让其一致

```shell
# 修改用户的bashrc文件
vi ~/.bashrc
# 在文件的底部加上一下命令
alias kubectl='minikube kubectl --'
```

