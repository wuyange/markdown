# Redis

## redis概述

### redis简介

https://try.redis.io/

https://www.redis.net.cn/tutorial/3502.html

### redis能做什么

Redis可以用于以下一些场景:

1. 缓存:网站热点数据、页面内容、API响应等经常访问的内容可以缓存在Redis中,大大减轻数据库压力,提高网站性能。
2. 聊天系统:Redis是实时聊天系统不错的选择,支持发布/订阅功能,可以实现聊天消息的实时推送。
3. 会话管理:用于保存会话相关数据,取代传统的文件或数据库来存储会话。
4. 应用排行榜:例如微博热榜,微信好友动态等,利用sorted set可以实现实时更新的排行功能。
5. 提交痕迹:利用List结构可以实现如点击列表的提交痕迹记录。
6. App排程任务:通过简单的LPUSH和BRPOP实现任务的队列调度。
7. 地图映射:利用Geo哈希存储地理位置的信息。
8. 网络状态监控:利用Keys用作主机状态报告的订阅-发布频道。
9. 高速缓存:与Memcached类似,用于加速动态网页或api内容。
10. 数据过期处理:Redis实现了存活时间,可以定期检查过期内存回收。
11. 分布式锁:利用SETNX实现分布式锁功能。

总之,Redis作为内存存储数据库,对实时性有需求的场景都很适用,比如社交、共享单车、快递送投等。

### 下载并安装redis

https://developer.aliyun.com/article/925491

```shell
# 下载docker镜像
docker pull redis:7.0

# 创建redis配置文件目录和数据文件目录
mkdir -p ~/redis/{conf,data}

# 下载redis配置文件
wget -O ~/redis/conf/redis6379.conf https://raw.githubusercontent.com/redis/redis/7.0/redis.conf

# 创建redis容器
docker run -d \
    --privileged=true \
    -p 6379:6379 \
    --name my-redis \
    -v ~/redis/conf/redis6379.conf:/etc/redis/redis.conf \
    -v ~/redis/data/6379:/data \
    redis:7.0 \
    redis-server /etc/redis/redis.conf \
    --appendonly yes
    
# 进入redis容器，查看redis版本
[root@localhost ~]# docker exec -it my-redis /bin/bash
root@2eae2ba4d39c:/data# redis-cli --version
redis-cli 7.0.13
```



配置文件

https://www.redis.net.cn/tutorial/3504.html

```
# 绑定地址 让其他主机也可以链接到本机的redis
bind 0.0.0.0

#  Redis默认不是以守护进程的方式运行，可以通过该配置项修改，使用yes启用守护进程
daemonize yes

# 指定Redis监听端口，默认端口为6379
port 6379

# 设置Redis连接密码
requirepass 123456
```



## redis命令

[英文命令文档](https://redis.io/commands/) [中文命令文档](https://www.redis.net.cn/order/)

**命令不区分大小写，而key是区分大小写的**

```shell
127.0.0.1:6379> set K1 v1
OK
127.0.0.1:6379> set k1 v1
OK
127.0.0.1:6379> keys *
1) "K1"
2) "k1"
127.0.0.1:6379> get k1
"v1"
127.0.0.1:6379> get K1
"v1"
127.0.0.1:6379> set K1 123
OK
127.0.0.1:6379> set k1 456
OK
127.0.0.1:6379> keys *
1) "K1"
2) "k1"
127.0.0.1:6379> get k1
"456"
127.0.0.1:6379> get K1
"123"
```

**帮助命令 help @类型**

```shell
127.0.0.1:6379> help @string

  APPEND key value
  summary: Append a value to a key
  since: 2.0.0

  DECR key
  summary: Decrement the integer value of a key by one
  since: 1.0.0
.....
127.0.0.1:6379> help @set

  SADD key member [member ...]
  summary: Add one or more members to a set
  since: 1.0.0

  SCARD key
  summary: Get the number of members in a set
  since: 1.0.0

  SDIFF key [key ...]
  summary: Subtract multiple sets
  since: 1.0.0

```

### 基本命令

#### 进入redis客户端

```shell
redis-cli -h 127.0.0.1 -p 6379 -a 123456 -n 0
# -h 127.0.0.1  redis服务器IP地址
# -p 6379  redis服务器端口
# -a 123456  redis服务器密码
# -n 0  redis服务器第几个数据库

root@1271388bcfb8:/data# redis-cli -h 10.185.5.86 -a 123456 -n 3
Warning: Using a password with '-a' or '-u' option on the command line interface may not be safe.
10.185.5.86:6379[3]>
```

#### redis键

**keys**：查看所有符合pattern的key

```shell
# 基本语法
KEYS PATTERN 

# 实例
127.0.0.1:6379> keys *
(empty array)
127.0.0.1:6379> set name xxx
OK
127.0.0.1:6379> set name1 xxx1
OK
127.0.0.1:6379> set value vi
OK
127.0.0.1:6379> keys name*
1) "name1"
2) "name"
127.0.0.1:6379> keys *
1) "name1"
2) "name"
3) "value"
```

**exists key**:命令用于检查给定key是否存在。

```shell
# 基本语法
EXISTS KEY_NAME

# 返回值
若 key 存在返回 1 ，否则返回 0 

# 实例
127.0.0.1:6379> exists name
(integer) 0
127.0.0.1:6379> set name vi
OK
127.0.0.1:6379> exists name
(integer) 1
```

**type key**:返回 key 所储存的值的类型

```shell
# 基本语法
TYPE KEY_NAME 

# 返回值
none (key不存在)
string (字符串)
list (列表)
set (集合)
zset (有序集)
hash (哈希表)

# 实例
127.0.0.1:6379> set k1 v1
OK
127.0.0.1:6379> type k1
string
127.0.0.1:6379> sadd pat dog
(integer) 1
127.0.0.1:6379> type pat
set
127.0.0.1:6379> type xxx
none
```

**del key**:删除指定的key数据

```shell
# 语法
DEL KEY_NAME [KEY_NAME...]

# 返回值
返回被成功删除的key的数量，删除不存在的key时会返回0

# 实例
127.0.0.1:6379> set k1 v1
OK
127.0.0.1:6379> set k2 v2
OK
127.0.0.1:6379> set k3 v3
OK
127.0.0.1:6379> set k4 v4
OK
127.0.0.1:6379> del k1
(integer) 1
127.0.0.1:6379> exists k1
(integer) 0
127.0.0.1:6379> del k2 k3
(integer) 2
127.0.0.1:6379> del k3
(integer) 0
127.0.0.1:6379> del k4 k5
(integer) 1
```

**ttl key**:以秒为单位，返回给定 key 的剩余生存时间
**pttl key**:以毫秒为单位，返回给定 key 的剩余生存时间
**expire key seconds** 为给定 key 设置过期时间

```shell
# 语法
TTL KEY_NAME
PTTL KEY_NAME
Expire KEY_NAME TIME_IN_SECONDS

# 返回值
ttl  以秒为单位返回 key 的剩余过期时间
pttl 以毫秒为单位，返回给定 key 的剩余生存时间
expire key seconds 为给定 key 设置过期时间
-1 表示永久有效
-2 表示已经过期

# 实例
127.0.0.1:6379> set k1 v1
OK
127.0.0.1:6379> ttl k1
(integer) -1
127.0.0.1:6379> expire k1 10
(integer) 1
127.0.0.1:6379> ttl k1
(integer) 7
127.0.0.1:6379> ttl k1
(integer) 4
127.0.0.1:6379> ttl k1
(integer) -2
127.0.0.1:6379> get k1
(nil)
```

**flashdb**:清除当前库中的所有内容
**flashall**:清除所有库中的所有内容
**select database_index**:切换数据库

```shell
# 实例
127.0.0.1:6379> set k1 v1
OK
127.0.0.1:6379> set k2 v2
OK
127.0.0.1:6379> keys *
1) "k2"
2) "k1"
127.0.0.1:6379> select 2
OK
127.0.0.1:6379[2]> set k1 v1
OK
127.0.0.1:6379[2]> keys *
1) "k1"
127.0.0.1:6379[2]> select 3
OK
127.0.0.1:6379[3]> set k3 v3
OK
127.0.0.1:6379[3]> set k4 v4
OK
127.0.0.1:6379[3]> keys *
1) "k4"
2) "k3"
127.0.0.1:6379[3]> FLUSHDB
OK
127.0.0.1:6379[3]> keys *
(empty array)
127.0.0.1:6379[3]> select 2
OK
127.0.0.1:6379[2]> keys *
1) "k1"
127.0.0.1:6379[2]> FLUSHALL
OK
127.0.0.1:6379[2]> keys *
(empty array)
127.0.0.1:6379[2]> select 0
OK
127.0.0.1:6379> keys *
(empty array)
```

### Redis字符串(string)



### Redis列表(list)

### Redis哈希(hash)

### Redis集合(set)

### Redis有序集合(zset)

### Redis位图(bitmap)

### Redis(hyperloglog)

### Redis地理位置空间(geo)