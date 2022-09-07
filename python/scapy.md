# Scapy模块

`Scapy`是一款强大的交互式数据包处理工具、数据包生成器、网络扫描器、网络发现、攻击工具和嗅探工具，能灵活地构造各种数据包、发送数据包、嗅探、应答和反馈匹配等功能。

## 下载和安装

```shell
pip install --pre scapy[basic]
```

提示如下信息表示安装成功

![image-20220807231516684](https://gitee.com/shunyu-online/shunyu_typora_image/raw/master/image/image-20220807231516684.png)

## 基础使用

### 更换主题

在实际开始使用`scapy`之前，可以通过修改 `conf.color_theme` 来切换主题

```python
# 提供以下可选主题
# DefaultTheme, BrightTheme, RastaTheme, ColorOnBlackTheme, BlackAndWhite, 
# HTMLTheme, LatexTheme

conf.color_theme = BrightTheme()
```

### 导入和导出

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

### 常用函数

```python
# ls() 查看支持的协议
# ls(SNMP)查看某个协议默认参数
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
>>> ls(SNMP)
version    : ASN1F_enum_INTEGER                  = ('0x1 <ASN1_INTEGER[1]>')
community  : ASN1F_STRING                        = ("<ASN1_STRING['public']>")
PDU        : ASN1F_CHOICE                        = ('\x1b[0m<\x1b[0m\x1b[31m\x1b[1mSNMPget\x1b[0m  \x1b[0m|\x1b[0m\x1b[0m>\x1b[0m')
    
# lsc() 列出scapy通用的操作方法
>>> lsc()
IPID_count          : Identify IP id values classes in a list of packets
arpcachepoison      : Poison target's cache with (your MAC,victim's IP) couple
arping              : Send ARP who-has requests to determine which hosts are up
arpleak             : Exploit ARP leak flaws, like NetBSD-SA2017-002.
bind_layers         : Bind 2 layers on some specific fields' values.
bridge_and_sniff    : Forward traffic between interfaces if1 and if2, sniff and return
chexdump            : Build a per byte hexadecimal representation
computeNIGroupAddr  : Compute the NI group Address. Can take a FQDN as input parameter
....
                                        
# pkt.summary()列出包的摘要 pkt可以是单个包，也可以是多个包组成的PacketList
# a为通过rdpcap导入的PacketList
>>> a.summary()
Ether / IP / TCP 10.231.3.236:49214 > 10.182.79.25:5044 S
Ether / IP / TCP 10.231.3.236:49214 > 10.182.79.25:5044 A
Ether / IP / TCP 10.231.3.236:49214 > 10.182.79.25:5044 PA / Raw
Ether / IP / TCP 10.231.3.236:49214 > 10.182.79.25:5044 A
Ether / IP / TCP 10.231.3.236:49214 > 10.182.79.25:5044 PA / Raw
Ether / IP / TCP 10.231.3.236:49214 > 10.182.79.25:5044 A
# a[0]表示通过rdpcap导入的PacketList中的第一个值
>>> a[0].summary()
'Ether / IP / TCP 10.231.3.236:49214 > 10.182.79.25:5044 S'

# pkt.show()展示包的开发视图
>>> a[0].show()
###[ Ethernet ]###
  dst       = 00:1c:54:52:28:89
  src       = 00:50:56:bc:04:1b
  type      = IPv4
###[ IP ]###
     version   = 4
     ihl       = 5
     tos       = 0x0
     len       = 52
     id        = 59978
     flags     = DF
     frag      = 0
     ttl       = 128
     proto     = tcp
     chksum    = 0x0
     src       = 10.231.3.236
     dst       = 10.182.79.25
     \options   \
###[ TCP ]###
        sport     = 49214
        dport     = 5044
        seq       = 2035854826
        ack       = 0
        dataofs   = 8
        reserved  = 0
        flags     = S
        window    = 64240
        chksum    = 0x68c8
        urgptr    = 0
        options   = [('MSS', 1460), ('NOP', None), ('WScale', 8), ('NOP', None), ('NOP', None), ('SAckOK', b'')]

# pkt.command() 以字符串的形式返回可生成数据包的scapy命令
# eval() 用来执行一个字符串表达式，并返回表达式的值。
>>> tmp = a[0].command()
"Ether(dst='00:1c:54:52:28:89', src='00:50:56:bc:04:1b', type=2048)/IP(version=4, ihl=5, tos=0, len=52, id=59978, flags=2, frag=0, ttl=128, proto=6, chksum=0, src='10.231.3.236', dst='10.182.79.25')/TCP(sport=49214, dport=5044, seq=2035854826, ack=0, dataofs=8, reserved=0, flags=2, window=64240, chksum=26824, urgptr=0, options=[('MSS', 1460), ('NOP', None), ('WScale', 8), ('NOP', None), ('NOP', None), ('SAckOK', b'')])"
>>> my_pkt = eval(tmp)
>>> my_pkt == a[0]
True
```



### 抓包

`sniff`函数简介

```python
sniff(filter=None,iface=None,count=0,prn=None,offline=None,stop_filter=None)
'''
以下为部分常用参数
count：抓包数量，默认为0，表示无限制
offline：读取 pcap 文件或者是文件列表，'/root/xxx.pcap' or ['/root/xxx.pcap','/root/xxx2.pcap']
prn：对每个数据包进行某个操作的函数。例如：prn = lambda x: x.summary()；
filter：不可以和offline一起使用
	BPF(Berkeley Packet Filter)过滤规则，wireshark过滤也使用的是BPF过滤器。
	dst host 192.168.0.1：目的IP为192.168.0.1的报文
	host 192.168.0.1：IP地址为192.168.0.1的报文
	tcp port 80：TCP端口号为80的报文（HTTP报文）
	tcp portrange 1-25：TCP端口范围1-25的报文
	not broadcast：排除广播报文
stop_filter：定义一个函数，在抓到指定数据包后停止抓包
iface：抓包的接口或者接口列表，'eth0' or ['eth0','eth1','eth2']
return：以PacketList的形式返回抓到的包
'''

# 异步抓包 AsyncSniffer 参数同sniff一样，在抓包期间还可以在命令行中干其他的事情
t = AsyncSniffer(prn=lambda x: x.summary(), filter="icmp")
t.start() # 开始抓包
t.stop()  # 结束抓包
t.results # 返回抓包结果
```

例子

```python
# 抓取两个源ip为10.182.79.36的icmp报文,并展示抓到的包的概要
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
                    
# 使用AsyncSniffer异步抓包期间输入hello world
>>> t = AsyncSniffer(filter='icmp and src host 10.182.79.36',prn=lambda x:x.summary())
>>> t.start()
Ether / IP / ICMP 10.182.79.36 > 10.231.3.236 echo-reply 0 / Raw
Ether / IP / ICMP 10.182.79.36 > 10.231.3.236 echo-reply 0 / Raw
Ether / IP / ICMP 10.182.79.36 > 10.231.3.236 echo-reply 0 / Raw
>>> print('hello world')
hello world
Ether / IP / ICMP 10.182.79.36 > 10.231.3.236 echo-reply 0 / Raw
Ether / IP / ICMP 10.182.79.36 > 10.231.3.236 echo-reply 0 / Raw
Ether / IP / ICMP 10.182.79.36 > 10.231.3.236 echo-reply 0 / Raw
>>> t.stop()
<Sniffed: TCP:0 UDP:0 ICMP:6 Other:0>
```

### 构造报文

#### 前置知识

```python
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

# 构造一个源IP为10.182.79.36 目的IP为10.182.79.35的IP报文
>>> my_ip = IP(src='10.182.79.36',dst='10.182.79.35')
<IP src=10.182.79.36 dst=10.182.79.35 |>

# 获取报文的字段值，如果报文的默认值没有被修改，Scapy会尝试为所有数据包字段使用合理的默认值
>>> my_ip.version
4

# 设置/修改报文的字段值
>>> my_ip.src = '10.182.79.38'
>>> my_ip.src
'10.182.79.38'

# 构建多层报文,这个 / 运算符用作两层之间的合成运算符,下层可以根据上层重载一个或多个默认字段
>>> my_tcp = TCP(dport=80,sport=9996)
>>> my_ip.proto
0
>>> my_pkt = my_ip / my_tcp
# 网络协议号中6表示tcp，可以通过[]取报文中某一层的数据
>>> my_pkt[IP].proto
6
>>> my_pkt.proto
6

# 一个数据包中可能有多层报文，不同层的报文中可能有相同的属性值
# 例如：链路层的Ether中有属性为src，网络层的IP中也有src
# 如果直接通过pkt.src的形式来取值，会取到下层中的src，也就是Ether报文的src
# 可以通过pkt[IP].src的形式来取IP报文中的src
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
>>> z = IP(ttl=[1,2,(8,10)])
>>> [i for i in z]
[<IP  ttl=1 |>,
 <IP  ttl=2 |>,
 <IP  ttl=8 |>,
 <IP  ttl=9 |>,
 <IP  ttl=10 |>]
>>> c = TCP(dport=[80,443])
# 所有字段之间使用笛卡尔积生成
>>> [i for i in z/c]
[<IP  frag=0 ttl=1 proto=tcp |<TCP  dport=http |>>,
 <IP  frag=0 ttl=1 proto=tcp |<TCP  dport=https |>>,
 <IP  frag=0 ttl=2 proto=tcp |<TCP  dport=http |>>,
 <IP  frag=0 ttl=2 proto=tcp |<TCP  dport=https |>>,
 <IP  frag=0 ttl=8 proto=tcp |<TCP  dport=http |>>,
 <IP  frag=0 ttl=8 proto=tcp |<TCP  dport=https |>>,
 <IP  frag=0 ttl=9 proto=tcp |<TCP  dport=http |>>,
 <IP  frag=0 ttl=9 proto=tcp |<TCP  dport=https |>>,
 <IP  frag=0 ttl=10 proto=tcp |<TCP  dport=http |>>,
 <IP  frag=0 ttl=10 proto=tcp |<TCP  dport=https |>>]
```

#### 构造ICMP报文

先通过`Scapy`抓一个真实的报文或者通过`rdpcap`导入一个真实的报文，然后通过`pkt.show()`展示报文的结构，按照报文结构一步一步的构造出数据包

```python
# 这里使用上面抓到的ICMP报文
>>> x[0].show()
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

### 发送报文

```python
# 只负责发送数据包，不接受报文
# send：发送3层数据包，不接收数据包，下面是部分参数
# send(x, iface=None, **kargs)
#     :param x: 被发送的数据包
#     :param inter: 发送两个包之间的时间间隔，以秒为单位，默认为0s
#     :param loop: 0 不循环发送，1 循环发送数据包，默认为0
#     :param count: 发送数据包的数量，默认为1
#     :param return_packets: 1 返回发送的数据包，0 不返回，默认为0
#     :param iface: 指定发送数据包的接口
#     :param verbose: verbose mode 默认为1，设置回显信息，设置为0，不显示回显

# sendp：发送2层数据包，不接收,使用方式基本和send一致

# 例
>>> pkt = send(my_pkt,loop=1,inter=2,count=3,return_packets=1)
...
Sent 3 packets.
>>> pkt
<PacketList: TCP:0 UDP:0 ICMP:3 Other:0>


# 发且收
# sr：发送/接收3层数据包，返回有回应的数据包和没有回应的数据包。
# sr1：发送3层数据包，只接收1个响应包
# srp：发送/接收2层数据包
# srp1：发送2层数据包，只接收1个响应包
# 上述四个使用方法都差不多
# sr(x, *args, **kargs)
#     :param x: 要发送的包
#     :param timeout: 设置超时时间，默认永不超时
#     :param verbose: 设置回显等级 0 没有回显 1 有回显，但是不那么详细  2 详细的回显,默认为2
#     return：返回两个值，第一个值为收到应答的包，第二个值为没有收到应答的包

# 例
# 构造一组ping包 10.182.79.36-39 其中10.182.79.39这个ip没有使用
my_ip = IP(dst='10.182.79.36/30',src='10.231.3.236')
my_icmp = ICMP()
my_load = 'abcdefghijklmnopqrstuvwabcdefghi'
my_pkt = my_ip / my_icmp / my_load

>>> ans, unans = sr(my_pkt,timeout=20)
Begin emission:
Finished sending 4 packets.
....*.**.............
Received 326 packets, got 3 answers, remaining 1 packets   # 收到3个回应，还有一个没有收到
>>> ans.summary() # 79.36,79.37,79.38都收到了回应
IP / ICMP 10.231.3.236 > 10.182.79.36 echo-request 0 / Raw ==> IP / ICMP 10.182.79.36 > 10.231.3.236 echo-reply 0 / Raw
IP / ICMP 10.231.3.236 > 10.182.79.37 echo-request 0 / Raw ==> IP / ICMP 10.182.79.37 > 10.231.3.236 echo-reply 0 / Raw
IP / ICMP 10.231.3.236 > 10.182.79.38 echo-request 0 / Raw ==> IP / ICMP 10.182.79.38 > 10.231.3.236 echo-reply 0 / Raw
>>> unans.summary() # 79.39没有收到
IP / ICMP 10.231.3.236 > 10.182.79.39 echo-request 0 / Raw

>>> ans = sr1(my_pkt,timeout=20,verbose=1)
Begin emission:
Finished sending 4 packets.
Received 269 packets, got 3 answers, remaining 1 packets  # 收到3个回应，还有一个没有收到
>>> ans.summary()    # 但是只保存一个有回应的包
'IP / ICMP 10.182.79.36 > 10.231.3.236 echo-reply 0 / Raw'
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







