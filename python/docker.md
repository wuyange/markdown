# docker模块

https://docker-py.readthedocs.io/en/stable/index.html

## 安装

```shell
pip install docker
```

## docker client

要与Docker守护进程通信，首先需要实例化一个客户端，有两种方式

- 最简单的方法是调用函数from_env()
- 可以通过实例化DockerClient类来手动配置

### dockers.from_env()

```python
# 返回当前环境下的docker客户端
dockers.from_env()
常用参数：	
timeout (int) – 设置超时时间，以秒为单位
max_pool_size (int) – 要保存在连接池中的最大连接数
assert_hostname (bool) – 验证服务器的主机名
use_ssh_client (bool) – 如果设置为True，则通过向ssh客户端发送ssh连接，确保主机上已安装并配置ssh客户端

import docker
client = docker.from_env()
```

### class DockerClient

一个与Docker服务器通信的客户端

```python
# 常用参数
base_url (str) – Docker服务器的url， unix:///var/run/docker.sock or tcp://127.0.0.1:1234.
timeout (int) – 设置超时时间，以秒为单位
user_agent (str) – 为发送给服务器的请求设置自定义用户代理
use_ssh_client (bool) – 如果设置为True，则通过向ssh客户端发送ssh连接，确保主机上已安装并配置ssh客户端
max_pool_size (int) – 要保存在连接池中的最大连接数

import docker
# 返回本地的docker客户端
client = docker.DockerClient(base_url='unix://var/run/docker.sock')
# 返回10.182.79.36的客户端
client = docker.DockerClient(base_url='http://10.182.79.36:2375')
```

#### 常用方法

```python
import docker
client = docker.DockerClient(base_url='unix://var/run/docker.sock')

# 关闭连接
# Closes all adapters and as such the session
client.close()

# 获取数据使用信息
# Get data usage information.
# 返回表示不同资源类别及其各自数据使用的字典。
# Returns type - dict:	A dictionary representing different resource categories and their respective data usage.
client.df()

# 从服务器获取实时事件。类似于docker events命令
# Get real-time events from the server. Similar to the docker events command.
client.events()
# 参数
since (UTC datetime or int) – 从某个时间获取事件
until (UTC datetime or int) – 一直到某个时间之前的事件
filters (dict) – 按事件时间、容器或筛选事件
decode (bool) – 如果设置为true, stream将被实时解码为dicts, 默认为False
Returns: 会返回一个生成器，如果没有指定until，就会一直等待新的事件产生
# 例子
>>> for event in client.events(decode=True)
...   print(event)
{u'from': u'image/with:tag',
 u'id': u'container-id',
 u'status': u'start',
 u'time': 1423339459}
...
or
>>> events = client.events()
>>> for event in events:
...   print(event)

# 显示整个系统的信息，和docker info命令返回结果一致，返回的数据类型是dict
client.info()

# 进行身份验证。类似于docker login命令
client.login()
# 常用参数
Parameters:	
username (str) – The registry username
password (str) – The plaintext password
email (str) – The email for the registry account
registry (str) – URL to the registry. E.g. https://index.docker.io/v1/
Returns: 返回值为dict
# 例子
>>> a.login(username='yushunfirst',password='YS@1293001619.asd')
{'username': 'yushunfirst', 'password': None, 'email': None, 'serveraddress': None}

# 检查服务器是否响应，返回值类型为bool
client.ping()

# 从服务器返回版本信息，类似于docker version命令，返回值类型为dict
client.version()
```

#### 属性

```python
client.configs
An object for managing configs on the server

client.containers
An object for managing containers on the server

client.images
An object for managing images on the server

client.networks
An object for managing networks on the server

client.nodes
An object for managing nodes on the server

client.plugins
An object for managing plugins on the server

client.secrets
An object for managing secrets on the server

client.services
An object for managing services on the server

client.swarm
An object for managing a swarm on the server

client.volumes
An object for managing volumes on the server
```

## docker configs

