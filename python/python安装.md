# python安装

centos7安装python3.11

```shell
cd /root
#只是将python3.11的安装包下载到 /root目录下
wget https://www.python.org/ftp/python/3.11.0/Python-3.11.0.tgz
#下载最新的软件安装包
tar -xzf Python-3.11.0.tgz
#解压缩安装包
yum -y install gcc zlib zlib-devel libffi libffi-devel
#安装源码编译需要的编译环境
yum install readline-devel
#可以解决后期出现的方向键、删除键乱码问题，这里提前避免。
yum install openssl-devel openssl11 openssl11-devel
#安装openssl11，后期的pip3安装网络相关模块需要用到ssl模块。
export CFLAGS=$(pkg-config --cflags openssl11)
export LDFLAGS=$(pkg-config --libs openssl11)
#设置编译FLAG，以便使用最新的openssl库
cd /root/Python-3.11.0
#进入刚解压缩的目录
./configure --prefix=/usr/python --with-ssl
#指定python3的安装目录为 /usr/python 并使用ssl模块，指定目录好处是
#后期删除此文件夹就可以完全删除软件了。
make
make install
#就是源码编译并安装了，时间会持续几分钟。
ln -s /usr/python/bin/python3 /usr/bin/python3
ln -s /usr/python/bin/pip3 /usr/bin/pip3
#指定链接，此后我们系统的任何地方输入python3就是我们安装的
#这个最新版python3了
```

centos7安装python3.7

```shell
1. 检查一下原来python的版本和是否有gcc
[root@loaclhost ~]# python -V
Python 2.7.5
[root@loaclhost ~]# gcc -version
-bash: gcc: 未找到命令
[root@loaclhost ~]# yum -y install gcc

2. python3.7以上版本，安装依赖包:libffi-devel
yum install gcc patch libffi-devel python-devel zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gdbm-devel db4-devel libpcap-devel xz-devel -y

3. wget下载python3.7.10
#安装wget
$yum install wget -y
#wget下载python3.7.10
$wget https://www.python.org/ftp/python/3.7.10/Python-3.7.10.tgz

4. 解压下载好的Python安装包
tar -zxvf Python-3.7.10.tgz

5. 进入解压后的目录，编译安装
#进入目录
$cd Python-3.7.10
#创建一个空文件夹，存放python3程序
$mkdir /usr/local/python3
#编译安装
$./configure --prefix=/usr/local/python3
$make && make install
./configure --prefix=/usr/local/python3执行完成时提示：那么再执行./configure --enable-optimization


6. 建立Python3的软连接
ln -s /usr/local/python3/bin/python3.7 /usr/bin/python3
ln -s /usr/local/python3/bin/pip /usr/bin/pip3

7. 检查Python3和pip3
[root@loaclhost Python-3.7.10]# python3
Python 3.7.10 (default, Mar 16 2022, 11:54:28) 
[GCC 4.8.5 20150623 (Red Hat 4.8.5-44)] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>>
[root@loaclhost Python-3.7.10]# pip3 --version
pip 22.0.4 from /usr/local/lib/python3.7/site-packages/pip (python 3.7)
```



设置pip源

```shell
mkdir ~/.pip
vi ~/.pip/pip.conf

# 内容如下
[global]
index-url = https://pypi.tuna.tsinghua.edu.cn/simple
[install]
trusted-host = https://pypi.tuna.tsinghua.edu.cn

pip3 config list 
```

