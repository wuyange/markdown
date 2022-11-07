# 安装k8s

1. 更新源并且安装https 以及curl

```shell
apt update && apt install -y apt-transport-https curl
```

2. 添加apt key源

```shell
curl -s https://mirrors.aliyun.com/kubernetes/apt/doc/apt-key.gpg | apt-key add - 
```

3. 更新缓存索引

```shell
cat <<EOF >/etc/apt/sources.list.d/kubernetes.list
deb https://mirrors.aliyun.com/kubernetes/apt/ kubernetes-xenial main
EOF
```

4. 再次更新源

```shell
apt update
```

5. 安装kubeadm、kubelet 和 kubectl

```shell
apt install kubectl kubelet kubeadm -y
```

6. docker需要和kubelet使用的是相同的 cgroup 驱动，推荐使用 `systemd` 驱动，查看docker的cgroup驱动

```shell
root@shunyu-virtual-machine:/etc/docker# docker info | grep -i "Cgroup Driver"
Cgroup Driver: cgroupfs
```

7. 修改/etc/docker/daemon.json文件，如果没有则新建

```shell
# 修改为以下内容
{
  "exec-opts": ["native.cgroupdriver=systemd"]
}
```

8. 修改kubelet的cgroup driver

```shell
# 新建一个配置文件 kubeadm-config.yaml
# kubeadm-config.yaml文件内容如下
kind: ClusterConfiguration
apiVersion: kubeadm.k8s.io/v1beta3
kubernetesVersion: v1.25.3
---
kind: KubeletConfiguration
apiVersion: kubelet.config.k8s.io/v1beta1
cgroupDriver: systemd

# 通过kubeadm config images list查看需要哪些镜像
root@master:/etc/docker# kubeadm config images list
registry.k8s.io/kube-apiserver:v1.25.3
registry.k8s.io/kube-controller-manager:v1.25.3
registry.k8s.io/kube-scheduler:v1.25.3
registry.k8s.io/kube-proxy:v1.25.3
registry.k8s.io/pause:3.8
registry.k8s.io/etcd:3.5.4-0
registry.k8s.io/coredns/coredns:v1.9.3

# 从国内镜像源拉取这些镜像
docker pull registry.cn-hangzhou.aliyuncs.com/google_containers/kube-apiserver:v1.25.3
docker pull registry.cn-hangzhou.aliyuncs.com/google_containers/kube-controller-manager:v1.25.3
docker pull registry.cn-hangzhou.aliyuncs.com/google_containers/kube-scheduler:v1.25.3
docker pull registry.cn-hangzhou.aliyuncs.com/google_containers/kube-proxy:v1.25.3
docker pull registry.cn-hangzhou.aliyuncs.com/google_containers/pause:3.8
docker pull registry.cn-hangzhou.aliyuncs.com/google_containers/etcd:3.5.4-0
docker pull registry.cn-hangzhou.aliyuncs.com/google_containers/coredns:1.9.3

# 对images重命名
docker tag registry.cn-hangzhou.aliyuncs.com/google_containers/kube-apiserver:v1.25.3 registry.k8s.io/kube-apiserver:v1.25.3
docker tag registry.cn-hangzhou.aliyuncs.com/google_containers/kube-controller-manager:v1.25.3 registry.k8s.io/kube-controller-manager:v1.25.3
docker tag registry.cn-hangzhou.aliyuncs.com/google_containers/kube-scheduler:v1.25.3 registry.k8s.io/kube-scheduler:v1.25.3
docker tag registry.cn-hangzhou.aliyuncs.com/google_containers/kube-proxy:v1.25.3 registry.k8s.io/kube-proxy:v1.25.3
docker tag registry.cn-hangzhou.aliyuncs.com/google_containers/pause:3.8 registry.k8s.io/pause:3.8
docker tag registry.cn-hangzhou.aliyuncs.com/google_containers/etcd:3.5.4-0 registry.k8s.io/etcd:3.5.4-0
docker tag registry.cn-hangzhou.aliyuncs.com/google_containers/coredns:1.9.3 registry.cn-hangzhou.aliyuncs.com/google_containers/coredns/coredns:v1.9.3

# 执行如下命令
kubeadm init --config kubeadm-config.yaml

# 输入了上面的命令后有可能提示kubeadm和部署控制平面版本不一致，按照提示信息的要求修改yaml文件中的版本号就可以了
```



8. 