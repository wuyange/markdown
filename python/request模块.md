# request模块

[Requests: 让 HTTP 服务人类 — Requests 2.18.1 文档 (python-requests.org)](https://docs.python-requests.org/zh_CN/latest/)

[浅谈requests库 - ShyButHandsome - 博客园 (cnblogs.com)](https://www.cnblogs.com/ShyButHandsome/p/12732132.html)

[HTTP 请求方法 - HTTP | MDN (mozilla.org)](https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Methods)

# 简介

requests是一个python的库，通过简单的api实现python对http请求的操作

# 安装

```shell
pip install requests
```

# 常用请求方法

```python
#GET请求一个指定资源
requests.get(url, params=None, **kwargs)

#HEAD和GET相同但是没有响应体
requests.head(url, **kwargs)

#POST用于将实体提交到指定的资源，通常导致在服务器上的状态变化或副作用
requests.post(url, data=None, json=None, **kwargs)

#PUT用请求有效载荷替换目标资源的所有
requests.put(url, data=None, **kwargs)

#PATCH方法用于对资源应用部分修改
requests.patch(url, data=None, **kwargs)

#DELETE删除指定的资源
requsets.delete(url, **kwargs) 

#可以构造上述任意的http方法，上述所有方法都是通过调用request()方法实现的
requests.request(method, url,params=None, data=None, headers=None, cookies=None, files=None,verify=None, cert=None, json=None,**kwargs)
```

# 响应

1. 通过GET/POST等方法构造一个Request对象，该对象将被发送到服务器以请求或查询某些资源
2. 一旦请求从服务器获得响应，就生成Response对象。Response对象包含服务器返回的所有信息，还包含最初创建的Request对象。

```python
r = requests.request('GET','https://10.182.83.14/api/webservice/system/info', verify=False)
print(r,type(r))
# 输出结果
<Response [200]> <class 'requests.models.Response'>
```

## 响应的常用属性

```python
# 响应状态码
print(type(r.status_code),r.status_code)
# <class 'int'> 200

# 响应的编码格式
print(type(r.encoding),r.encoding)
# <class 'str'> UTF-8

# 返回响应体中的内容
print(type(r.text),r.text)
# <class 'str'> {
#	"geo_version":"1.0.210526",
#	"version":"V2.0R6",
#	.....
#	"locale":"zh_CN"
#}

# 返回请求的url信息
print(type(r.url),r.url)
# <class 'str'> https://10.182.83.14/api/webservice/system/info

# 以字节的形式返回的响应体中的内容
print(type(r.content),r.content)
<class 'bytes'>b'{\n\t"geo_version":"1.0.210526",\n\t"version":"V2.0R6",\n\t"platform":"SG-6000-ISC6205",\n\t"cpuNum":20,\n\t"clusterSize":1,\n\t"uptime":1640166191000,\n\t"hostname":"b9de88a186",\n\t"rule_version":"1.0",\n\t"zone":"Shanghai",\n\t"vm":false,\n\t"memoryTotal":134633631744,\n\t"sn":"419139989",\n\t"time":1643181292224,\n\t"diskMap":{\n\t\t"sda":5999999057920\n\t},\n\t"lib_dns_version":"2.0.220125",\n\t"lib_malcode_version":"2.0.220125",\n\t"lib_ip_version":"2.0.220125",\n\t"lib_vuln_version":"2.0.201210",\n\t"lib_log_parse_config_version":"1.1.210926",\n\t"ips_version":"2.0.2",\n\t"locale":"zh_CN"\n}'

# 处理json格式的响应内容
print(type(r.json()),r.json())
<class 'dict'> {'geo_version': '1.0.210526', 'version': 'V2.0R6', 'platform': 'SG-6000-ISC6205', 'cpuNum': 20, 'clusterSize': 1, 'uptime': 1640166191000, 'hostname': 'b9de88a186', 'rule_version': '1.0', 'zone': 'Shanghai', 'vm': False, 'memoryTotal': 134633631744, 'sn': '419139989', 'time': 1643181292224, 'diskMap': {'sda': 5999999057920}, 'lib_dns_version': '2.0.220125', 'lib_malcode_version': '2.0.220125', 'lib_ip_version': '2.0.220125', 'lib_vuln_version': '2.0.201210', 'lib_log_parse_config_version': '1.1.210926', 'ips_version': '2.0.2', 'locale': 'zh_CN'}

# 被请求的服务器的响应头的内容
print(type(r.headers),r.headers)

# 原始的请求中的所有内容
print(type(r.request),r.request)
# r.request.body 获取请求体中的内容
# r.request.headers 获取请求头中的内容
# r.request.method 获取请求方法
# r.request.url 获取请求得url

# 会话中携带的cookies信息
print(r.cookies)
<RequestsCookieJar[<Cookie token=3c38d12a71e746a99ede2920c0949645 for 10.182.79.25/>, <Cookie userInfo=%7B%22generation%22%3A1%2C%22id%22%3A3%2C%22lastVisitTime%22%3A1665215739054%2C%22passwordTimeoutStartDate%22%3A%222022-06-15%22%2C%22role%22%3A%22admin%22%2C%22token%22%3A%223c38d12a71e746a99ede2920c0949645%22%2C%22userName%22%3A%22shunyu1%22%7D for 10.182.79.25/>]>
print(r.cookies['token'])
3c38d12a71e746a99ede2920c0949645
```

# GET请求传参

```python
import json
query = {'q':'山石'}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
}
r = requests.request("get",url="https://www.zhihu.com/api/v4/search/suggest",params = query,verify=False,headers=headers)
print(r.url)
print(json.dumps(r.json(),ensure_ascii=False,indent=4))
#输出结果
https://www.zhihu.com/api/v4/search/suggest?q=%E5%B1%B1%E7%9F%B3
{
    "suggest": [
        {
            "query": "山石网科",
            "id": 4852906456497459199,
            "raw_id": "4852906456497459199"
        },
        {
            "query": "山石网科怎么样",
            "id": 4552204018898346981,
            "raw_id": "4552204018898346981"
        },
    	....
        {
            "query": "山石韩愈",
            "id": -1889167879302081315,
            "raw_id": "-1889167879302081315"
        }
    ],
    "input_hash_id": "231c3d1b1b657b240a6ac97b9f266d4f",
    "attached_info": "OiOCAyAyMzFjM2QxYjFiNjU3YjI0MGE2YWM5N2I5ZjI2NmQ0Zg=="
}
```

# 携带数据的POST请求

## 使用data传递数据

常见的form表单 使用data传递数据

```python
# 常见的form表单 使用data传递数据
data = {"userName":"shunyu1","password":"QUFiYjExISE="}
r = requests.request('post',url = "https://10.182.79.25/api/webservice/user/sso/login", data=data,verify=False)
print(r.status_code)
#输出结果
200
```

## 使用json传递数据

**如果指定了data参数 那么json参数就会失效**

```python
# 对于json数据 使用json传递数据
# 如果指定了data参数 那么json参数就会失效
data = {"userName":"shunyu","password":"QUFiYjExISE=","validateCode":"aaaa"}
r = requests.request("post", url = "https://10.182.79.25/api/webservice/user/login", json=data,verify=False)
print(r.text)
# 输出结果
{
    "result": {
        "department": "Hillstone Networks",
        "description": "Default account",
        "generation": 0,
        "id": 1,
        "lastVisitTime": 1665212665203,
        "notifyDate": "",
        "password": "",
        "passwordModificationDate": "2022-06-15",
        "passwordTimeoutStartDate": "2022-06-15",
        "role": "admin",
        "token": "e9785d92b2dd49b3adcc029857b64a1d",
        "userName": "hillstone"
    },
    "total": 0
}
```

# 上传文件

```python
url = 'https://httpbin.org/post'
files = {'file': open('report.xls', 'rb')}

r = requests.post(url, files=files)
r.text
{
  ...
  "files": {
    "file": "<censored...binary...data>"
  },
  ...
}

# 显式地设置文件名、content_type和头文件:
url = 'https://httpbin.org/post'
files = {'file': ('report.xls', open('report.xls', 'rb'), 'application/vnd.ms-excel', {'Expires': '0'})}

r = requests.post(url, files=files)
r.text
{
  ...
  "files": {
    "file": "<censored...binary...data>"
  },
  ...
}
```

# 下载二进制文件

```python
r = requests.request("GET",url = "https://static.zhihu.com/heifetz/assets/loginBackgroundImg.2c81e205.png", verify=False)
print(r.content)
with open('xxx.png',"wb") as fp:
    fp.write(r.content)
```

# Cookies

## 获取请求中的cookies

```python
data = {"userName":"shunyu1","password":"QUFiYjExISE="}
r = requests.request('post',url = "https://10.182.79.25/api/webservice/user/sso/login", data=data,verify=False,json={})
print(r.cookies)
<RequestsCookieJar[<Cookie token=3c38d12a71e746a99ede2920c0949645 for 10.182.79.25/>, <Cookie userInfo=%7B%22generation%22%3A1%2C%22id%22%3A3%2C%22lastVisitTime%22%3A1665215739054%2C%22passwordTimeoutStartDate%22%3A%222022-06-15%22%2C%22role%22%3A%22admin%22%2C%22token%22%3A%223c38d12a71e746a99ede2920c0949645%22%2C%22userName%22%3A%22shunyu1%22%7D for 10.182.79.25/>]>
print(r.cookies['token'])
3c38d12a71e746a99ede2920c0949645
```

## 请求时携带Cookie

```python
url = 'https://httpbin.org/cookies'
cookies = dict(cookies_are='working')
r = requests.get(url, cookies=cookies)
print(r.text)
# 输出结果
'{"cookies": {"cookies_are": "working"}}'
```

## 构造cookies

```python
url = 'https://httpbin.org/cookies'
jar = requests.cookies.RequestsCookieJar()
jar.set('tasty_cookie', 'yum', domain='httpbin.org', path='/cookies')
jar.set('gross_cookie', 'blech', domain='httpbin.org', path='/elsewhere')
url = 'https://httpbin.org/cookies'
r = requests.get(url, cookies=jar)
print(r.text)
# 输出结果
# 因为在/cookies路径下，所以只传递了tasty_cookie
'{"cookies": {"tasty_cookie": "yum"}}'
```

# 重定向

response.history包含为了完成请求而创建的Response对象,列表从最老的到最近的回答排序。

设置allow_redirects=False可以禁止重定向

默认情况下，请求将对除HEAD之外的所有请求执行位置重定向。

```python
# GitHub将所有HTTP请求重定向到HTTPS
r = requests.get('http://github.com/')
print(r.url)
'https://github.com/'
print(r.history)
[<Response [301]>]

# 设置allow_redirects=False可以禁止重定向
r = requests.get('http://github.com/', allow_redirects=False)
print(r.status_code)
301
print(r.history)
[]

# 设置allow_redirects=True可以使head重定向
r = requests.head('http://github.com/', allow_redirects=True)
print(r.url)
'https://github.com/'
print(r.history)
[<Response [301]>]
```

# Session

Session对象允许跨请求持久化某些参数。它还跨所有来自Session实例的请求持久化cookie，并将使用urllib3的连接池。因此，如果向同一个主机发出多个请求，则底层TCP连接将被重用，这将显著提高性能。

```python
#会话session()
#会话对象让你能够跨请求保持某些参数,它会在同一个 Session 实例发出的所有请求之间保持 cookie
s = requests.session()
# 登录
data = {"userName":"shunyu1","password":"QUFiYjExISE="}
s.request('post',url = "https://10.182.79.25/api/webservice/user/sso/login", data=data,verify=False,json={})
print(r.text)
#输出结果
{
	"result":{
		"department":"",
		"description":"",
		"generation":1,
		"id":10,
		"lastVisitTime":1643249610492,
		"notifyDate":"",
		"password":"",
		"passwordModificationDate":"",
		"passwordTimeoutStartDate":"2021-12-01",
		"role":"readonly",
		"token":"1d5617f1213148849238842722f1bb6a",
		"userName":"shunyu1"
	},

# 删除资产
query = {'query': {"conditions":[{"field":"timestamp","value":{"start":1640657534000,"end":1643249534000},"operator":8,"logical":1}]}}
r = s.request("get",url = "https://10.182.79.25/api/webservice/monitor/overview/hotEvents", params=query, verify=False)
print(r.text)
#输出结果
{
	"result":[
		"123",
		"恶意软件",
		"拒绝服务",
		"web application scan",
		"11",
		"☠",
		"蹻6#3叅螷uS&9毴</div>gIX.44@12%^B106c8龁槢42^鍾5]]&o沔ed*E黲$9e<26齳?j蹻6#3叅螷uS&9毴</div>gIX.44@12%^B106c8龁槢42^鍾5]]&o沔ed*E黲$9蹻6#3叅螷uS&9毴</div>gIX.44@12%^B106c8龁槢42^鍾5]]&o沔ed*E黲$9蹻6#3叅螷uS&9毴</div>gIX.44@12%^B106c8龁槢42^鍾5]]&o沔ed*E黲$9蹻6#3叅螷uS&9毴</div>gIX.44@12%^B106c8龁槢42^鍾5]]&o沔ed*E黲$9蹻6#3叅螷uS&9毴</div>gIX.44@12%^B106c8龁槢42^鍾5]]&o沔ed*E黲$98薾8:46<Y[",
		"垃圾邮件",
		"mal_url/grouptightener",
		"Bulk Spam"
	],
	"total":10
}
```

# SSL

默认情况下，SSL验证是启用的，如果无法验证证书，请求将抛出SSLError

```python
requests.get('https://10.182.79.25')
# ax retries exceeded with url: / (Caused by SSLError(SSLCertVerificationError(1, '[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:997)')))
```

可以通过设置verify=False，使请求时不验证证书是否有效，默认值是 True

```python
requests.get('https://10.182.79.25', verify=False)
```

设置verify=False后，会有告警，可以通过以下方式忽略告警

```python
# 方式1
import requests
from requests.packages import urllib3
urllib3.disable_warnings()
requests.get('https://10.182.79.25', verify=False)

# 方式2
import warnings
warnings.filterwarnings("ignore")
import requests
requests.get('https://10.182.79.25', verify=False)
```

# 代理

如果需要使用代理，可以用代理参数配置单个请求的任何请求方法

```python
import requests

proxies = {
  'http': 'http://10.10.1.10:3128',
  'https': 'http://10.10.1.10:1080',
}

requests.get('http://example.org', proxies=proxies)
```

