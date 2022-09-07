# docker存储

docker为容器提供了两种存放数据的资源

- 由 `storage driver` 管理的镜像层和容器层
- `data volume`

## storage driver

容器由最上面的可写容器层，以及若干只读的镜像层组成，这样的分层结果最大的特性就是 `Copy-on-Write` 

- 新数据会直接存放在最上面的容器层
- 修改现有的数据会先从镜像层将数据复制到容器层，修改后的数据直接保存在容器层中，镜像层保持不变
- 如果多个层中有命名相同的文件，用户只能看到最上面那层中的文件

`docker` 的分层结构要归功于 `docker storage driver`  正是`storage driver` 实现了多测数据的堆叠，并为用户提供一个单一的合并后的统一视图

`docker` 支持多种`storage driver`，有`AUFS`、`Device Mapper`、`Btrfs`、`OverlayFs`、`VFS`和`ZFS`，他们都可以实现分层的架构，同时又有各自的特性，`docker`官方建议优先使用`Linux`发行版默认的`storage driver`，`docker`安装时会根据当前系统的配置选择默认的`driver`

使用`docker info` 查看`linux`上的默认`driver`和底层文件系统

```shell
root@ubuntu:~# docker info |grep -A 3 -i storage
 Storage Driver: overlay2
  Backing Filesystem: extfs
  Supports d_type: true
  Native Overlay Diff: true

root@ubuntu:/var/lib/docker/overlay2# docker info |grep -i 'root dir'
 Docker Root Dir: /var/lib/docker
```

`ubuntu`默认使用的`driver`是`AUFS`，底层文件系统是`extfs`，各层数据存放在`/var/lib/docker/overlay2`

- 对于那些无状态的容器，直接将数据放在`storage driver`维护的层中是很好的选择，无状态意味着容器没有需要持久化的数据，如`busybox`
- 对于有持久化数据的需求，容器启动时需要家长已有的数据，容器销毁时希望保留生产的新数据，需要使用`docker`的另一种存储机制 `data volume`

## Data Volume

`data volume`本质上是`docker host`文件系统中的目录或者文件能直接被 `mount`到容器的文件系统中

- `data volume` 是目录或者文件，而不是没有格式化的磁盘
- 容器可以读写`volume`中的数据
- `volume`数据可以永久的保存

`docker`提供了两种类型的`volume`

- `bind mount`
- `docker managed volume`

### bind mount

`bind mount`是将`host`上已存在的目录或文件`mount`到容器

通过`-v  <host path>:<container path>`实现

```shell
root@ubuntu:~# mkdir httpdir
root@ubuntu:~/httpdir# vim httpdir/index.html

# 添加下面的内容
<!DOCTYPE html>
<html lang="cn">
<head>
    <meta charset="UTF-8">
    <title>Document</title>
</head>
<body>
    <h1>这是docker文件里面</h1>
</body>
</html>

# 运行容器
root@ubuntu:~# docker run -d -p 80:80 -v /root/httpdir/:/usr/local/apache2/htdocs httpd
c2faf17369825dafcbd802e7d2c7ce29418508b06db3ba43032a5a120ab3c420

# 访问httpd
root@ubuntu:~/httpdir# curl 127.0.0.1:80
<!DOCTYPE html>
<html lang="cn">
<head>
    <meta charset="UTF-8">
    <title>Document</title>
</head>
<body>
    <h1>这是docker文件里面</h1>
</body>
</html>

# 在host主机中修改index.html文件
root@ubuntu:~/httpdir# vim index.html
root@ubuntu:~/httpdir# cat index.html
<!DOCTYPE html>
<html lang="cn">
<head>
    <meta charset="UTF-8">
    <title>Document</title>
</head>
<body>
    <h1>这是更新后的文件内容</h1>
</body>
</html>

# 访问httpd
root@ubuntu:~/httpdir# curl 127.0.0.1:80
<!DOCTYPE html>
<html lang="cn">
<head>
    <meta charset="UTF-8">
    <title>Document</title>
</head>
<body>
    <h1>这是更新后的文件内容</h1>
</body>
</html>

# 删除容器
root@ubuntu:~/httpdir# docker stop c2faf1736982
c2faf1736982
root@ubuntu:~/httpdir# docker rm c2faf1736982
c2faf1736982
root@ubuntu:~/httpdir# cat index.html
<!DOCTYPE html>
<html lang="cn">
<head>
    <meta charset="UTF-8">
    <title>Document</title>
</head>
<body>
    <h1>这是更新后的文件内容</h1>
</body>
</html>
# 可见删除容器并不会删除host中被挂载的文件和目录还在
```

`bind mount`还可以设置数据的读写权限，默认是可读可写的，可设定为只读

```shell
root@ubuntu:~/httpdir# docker run -d -p 80:80 -v /root/httpdir:/usr/local/apache2/htdocs:ro httpd
026cb27b5c5814559e30e24a0590313f89b8ac2fc798f47af5bd443d6d975716
root@ubuntu:~/httpdir# docker ps -q
026cb27b5c58
1419b9c64c48
d4156c3dc564
root@ubuntu:~/httpdir# docker exec -it 026cb27b5c58 /bin/bash
root@026cb27b5c58:/usr/local/apache2# echo 'xxxxx' > /usr/local/apache2/htdocs/index.html
bash: /usr/local/apache2/htdocs/index.html: Read-only file system
```

除了`bind mount`目录之外，还可以单独指定一个文件

- 这样可以只向容器添加文件，而不修改容器原有的内容
- 指定单个文件时要确保文件是存在的，不然会当成一个新目录挂载

```shell
root@ubuntu:~/httpdir# docker run -d -p 80:80 -v /root/httpdir/index.html:/usr/local/apache2/htdocs/new.html httpd
80d9c89fb88d77fcc27337ea75e5d41bc5d025da9df1f5babcdcb423c1231752
root@ubuntu:~/httpdir# curl 127.0.0.1:80
<html><body><h1>It works!</h1></body></html>
root@ubuntu:~/httpdir# curl 127.0.0.1:80/new.html
<!DOCTYPE html>
<html lang="cn">
<head>
    <meta charset="UTF-8">
    <title>Document</title>
</head>
<body>
    <h1>这是更新后的文件内容</h1>
</body>
</html>

# 指定单个文件时要确保文件是存在的，不然会当成一个新目录挂载
root@ubuntu:~/httpdir# docker run -d -p 80:80 -v /root/httpdir/new_index.html:/usr/local/apache2/htdocs/new.html httpd
6ad778641a672bc2398bfdd8c496aaea003430df4447a4e6c44f3f71739f5ea9
root@ubuntu:~/httpdir# ll
total 16
drwxr-xr-x  3 root root 4096 May 31 21:31 ./
drwx------ 13 root root 4096 May 31 20:29 ../
-rw-r--r--  1 root root  170 May 31 20:29 index.html
drwxr-xr-x  2 root root 4096 May 31 21:31 new_index.html/
```

### docker managed volume

`docker managed volume`和`bind mount`的区别在于不需要制定`mount`源

```shell
root@ubuntu:~/httpdir/new_index.html# docker run --name http -d -p 80:80 -v /usr/local/apache2/htdocs httpd
a8082a869c286b6059890c5686a10f63c94d0fc65241840b99b7f3c966b03b76
root@ubuntu:~/httpdir/new_index.html# docker inspect http | grep -A 11 -i "Mounts"
        "Mounts": [
            {
                "Type": "volume",
                "Name": "ecaa39bc65188ffc559a9c5050665080324deed3f5a32b62972e52efafd5dd64",
                "Source": "/var/lib/docker/volumes/ecaa39bc65188ffc559a9c5050665080324deed3f5a32b62972e52efafd5dd64/_data",
                "Destination": "/usr/local/apache2/htdocs",
                "Driver": "local",
                "Mode": "",
                "RW": true,
                "Propagation": ""
            }
        ]
# 容器数据存储在/var/lib/docker/volumes/ecaa39bc65188ffc559a9c5050665080324deed3f5a32b62972e52efafd5dd64/_data中
# 如果-v后面跟的目录是一个已有目录，则原有的数据就会诶复制到/var/lib/docker/volumes/文件夹下
# 可以使用docker volume ls 查看容器数据存储而位置，但是无法知道对应的容器，而且看不到bind mount的内容
root@ubuntu:~# docker volume ls
DRIVER    VOLUME NAME
local     5c13ddf73500d5d87a6895ba9cb21a1a438fd44a0c1ac17544e1c03cd083baad
local     8e7ae31f30064a3f3066e59cca60d957a310572af350b46e6cf6037a4c27abd6
```

![image-20220608204927214](C:\Users\shunyu\AppData\Roaming\Typora\typora-user-images\image-20220608204927214.png)

## 数据共享

### 容器与host共享数据

- `bind mount`:直接将要共享的目录mount到容器
- `docker managed volume`:在容器启动后，将要共享的数据复制到`/var/lib/docker/volumes/`文件夹下
  - 也可以使用`docker cp 要共享的文件 容器短ID:容器中文件的位置`

### 容器之间共享数据

- 多个容器`mount`在一个`host`文件夹下

```shell
root@ubuntu:~# docker run -d -p 81:80 -v /root/httpdir/new_index.html:/usr/local/apache2/htdocs/new.html httpd
64f4c1ca40130b07c813317a466438c5c3860366ea8bcfa2047381ce24007120
root@ubuntu:~# docker run -d -p 82:80 -v /root/httpdir/new_index.html:/usr/local/apache2/htdocs/new.html httpd
307602ed744631c0fdea084056a3deb601fad42cef246ebada121553f7bca304
root@ubuntu:~# docker run -d -p 83:80 -v /root/httpdir/new_index.html:/usr/local/apache2/htdocs/new.html httpd
58803b14feae966da36497694ad709959df22a94731342b3ef642906353c2320
root@ubuntu:~# curl 10.182.79.36:81
<html><body><h1>这是host</h1></body></html>
root@ubuntu:~# curl 10.182.79.36:82
<html><body><h1>这是host</h1></body></html>
root@ubuntu:~# curl 10.182.79.36:83
<html><body><h1>这是host</h1></body></html>
```

### volume container

`volume container`是专门为其他容器提供`volume`的容器，它提供的卷可以是`bind mount` 也可以是`docker managed volume`

```shell
root@ubuntu:~# docker create --name vc_data -v /root/httpdir/new_index.html:/usr/local/apache2/htdocs/new.html -v /root/httpdir/index.html busybox
d096392938dd1fc82153f35a6c94eaab27e05ebfc3bcdee655604d9f14a25026
root@ubuntu:~# docker inspect vc_data | grep -A 19 -i "Mounts"
        "Mounts": [
            {
                "Type": "bind",
                "Source": "/root/httpdir/new_index.html",
                "Destination": "/usr/local/apache2/htdocs/new.html",
                "Mode": "",
                "RW": true,
                "Propagation": "rprivate"
            },
            {
                "Type": "volume",
                "Name": "a9c3d42a9946fdf2ad0513456839f5783aeff666632fe48fa1e4d4b69dbd7a86",
                "Source": "/var/lib/docker/volumes/a9c3d42a9946fdf2ad0513456839f5783aeff666632fe48fa1e4d4b69dbd7a86/_data",
                "Destination": "/root/httpdir/index.html",
                "Driver": "local",
                "Mode": "",
                "RW": true,
                "Propagation": ""
            }
        ],
        
# 其他容器可以通过--volumes-from使用volume container
root@ubuntu:~/httpdir/new_index.html# docker run --name web1 -d -p 84:80 --volumes-from vc_data httpd
9515b872c81fdb7c6e6e3fe72414183d3abcf0d33e617b52a377c106a3a95afc
root@ubuntu:~/httpdir/new_index.html# curl 10.182.79.36:84/new.html/
这是host
root@ubuntu:~/httpdir/new_index.html# docker inspect web1 | grep -A 19 -i "Mounts"
        "Mounts": [
            {
                "Type": "bind",
                "Source": "/root/httpdir/new_index.html",
                "Destination": "/usr/local/apache2/htdocs/new.html",
                "Mode": "",
                "RW": true,
                "Propagation": "rprivate"
            },
            {
                "Type": "volume",
                "Name": "a9c3d42a9946fdf2ad0513456839f5783aeff666632fe48fa1e4d4b69dbd7a86",
                "Source": "/var/lib/docker/volumes/a9c3d42a9946fdf2ad0513456839f5783aeff666632fe48fa1e4d4b69dbd7a86/_data",
                "Destination": "/root/httpdir/index.html",
                "Driver": "local",
                "Mode": "",
                "RW": true,
                "Propagation": ""
            }
        ],
        
# 再起两个容器，发现web1,web2,web3这三个容器的数据都是共享数据的
root@ubuntu:~/httpdir/new_index.html# docker run --name web2 -d -p 85:80 --volumes-from vc_data httpd
82969f29c7d3fa2f9b43af5a31f55243945f213f9f1f5bf4bef348e5cbd2f387
root@ubuntu:~/httpdir/new_index.html# docker run --name web3 -d -p 86:80 --volumes-from vc_data httpd
0cd5a745383781b8418691b3c7f433ac6763a7008dd629b19f9335b9af12899b
root@ubuntu:~/httpdir/new_index.html# curl 10.182.79.36:85/new.html/
这是host
root@ubuntu:~/httpdir/new_index.html# curl 10.182.79.36:86/new.html/
这是host
# 编辑host中的/usr/local/apache2/htdocs/new.html
root@ubuntu:~/httpdir/new_index.html# vim index.html
root@ubuntu:~/httpdir/new_index.html# curl 10.182.79.36:85/new.html/
这是host
update
root@ubuntu:~/httpdir/new_index.html# curl 10.182.79.36:84/new.html/
这是host
update
```

- `volume container`与`bind mount`相比，不必为每一个容器指定`host path`，所有的`path`都在`volume container`中定义好了，容器只需要与`volume container`关联，实现了容器和`host`的解耦

### data-packed volume container

`data-packed volume container`将数据打包到镜像中，然后通过`docker managed volume`共享

```shell
# 新建一个文件夹htdoc，并且在其中新建一个文件index.html,内容如下
这个是容器内部的数据

# 编写dockerfile，内容如下
root@ubuntu:~/docker/dockerfile# vim dockerflie
root@ubuntu:~/docker/dockerfile# cat dockerflie
from busybox:latest
ADD htdocs /usr/local/apache2/htdocs
volume /usr/local/apache2/htdocs

# build dockerfile文件，并创建容器
root@ubuntu:~/docker/dockerfile# docker build -t vc_data . -f ./dockerflie
Sending build context to Docker daemon  18.43kB
Step 1/3 : from busybox:latest
 ---> 1a80408de790
Step 2/3 : ADD htdocs /usr/local/apache2/htdocs
 ---> ffeb1f47cf21
Step 3/3 : volume /usr/local/apache2/htdocs
 ---> Running in 900e962fa70e
Removing intermediate container 900e962fa70e
 ---> 2cce68df570d
Successfully built 2cce68df570d
Successfully tagged vc_data:latest
root@ubuntu:~/docker/dockerfile# docker create --name vc_data vc_data
00bd8fd5c1a620137f0bca6af2bfd360a17508bb7b3e1a5fbd7868a66e2d1510

root@ubuntu:~/docker/dockerfile# docker run -d -p 82:80 --volumes-from vc_data httpd
8d536e9860f21b8870865b0110f80a7a892b27ddb2b61f07264b159f4dabf8b7
root@ubuntu:~/docker/dockerfile# curl 10.182.79.36:82
这个是容器内部的数据

root@ubuntu:~/docker/dockerfile# docker run -d -p 83:80 --volumes-from vc_data httpd
b4bb3eb6afdfc203cadcc22f88a17bd34d580181629336233802a5b0b1ecc35d
root@ubuntu:~/docker/dockerfile# docker exec -it b4bb3eb6af /bin/bash
root@b4bb3eb6afdf:/usr/local/apache2# ls
bin  build  cgi-bin  conf  error  htdocs  icons  include  logs  modules
root@b4bb3eb6afdf:/usr/local/apache2# cd htdocs/
root@b4bb3eb6afdf:/usr/local/apache2/htdocs# ls
index.html
root@b4bb3eb6afdf:/usr/local/apache2/htdocs# touch new.html
root@b4bb3eb6afdf:/usr/local/apache2/htdocs# echo 'hahaha' > new.html
root@b4bb3eb6afdf:/usr/local/apache2/htdocs# exit
exit
root@ubuntu:~/docker/dockerfile# curl 10.182.79.36:82/new.html
hahaha
root@ubuntu:~/docker/dockerfile# curl 10.182.79.36:83
这个是容器内部的数据
```

>容器能够正确读取 volume 中的数据。data-packed volume container 是自包含的，不依赖 host 提供数据，具有很强的移植性，非常适合 只使用静态数据的场景，比如应用的配置信息、web server 的静态文件等。

## Data volume生命周期管理

### 备份

因为`volume`实际上时`host`文件系统中的目录和文件，所以`volume`的备份实际上是对文件系统的备份，所有的本地镜像都保存在`host`主机的`/myregistry`目录中

### 恢复

如果数据损坏了，直接用之前的备份的数据，复制到`/myregistry`目录

### 迁移

如果想使用更新版本的registry

- `docker stop`当前`registry`容器
- 启动新版本容器并`mount`原有`volume`

### 销毁

- `docker`不会销毁`bind mount`,删除数据的工作只能由`host`负责

- 删除`docker managed volume`，需要在使用`docker rm`时带上`-v`参数
  - 如果有多个容器都在使用这个`volume`，则不会删除
  - 如果删除容器时没有携带`-v`参数，就会产生孤儿`volume`，可以使用`docker managed ls`查看到，可以使用`docker volume rm`删除
  - 批量删除孤儿`volume`    `docker volume rm $(docker volume ls -q)`

