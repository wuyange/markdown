# request模块

[Requests: 让 HTTP 服务人类 — Requests 2.18.1 文档 (python-requests.org)](https://docs.python-requests.org/zh_CN/latest/)

[浅谈requests库 - ShyButHandsome - 博客园 (cnblogs.com)](https://www.cnblogs.com/ShyButHandsome/p/12732132.html)

[HTTP 请求方法 - HTTP | MDN (mozilla.org)](https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Methods)

```python
#简介
#requests是一个python的库，通过简单的api实现python对http请求的操作

#安装
pip install requests
 
#常用方法
requests.get(url, params=None, **kwargs)               #GET请求一个指定资源
requests.head(url, **kwargs)                           #HEAD和GET相同但是没有响应体
requests.post(url, data=None, json=None, **kwargs)     #POST用于将实体提交到指定的资源，通常导致在服务器上的状态变化或副作用
requests.put(url, data=None, **kwargs)                 #PUT用请求有效载荷替换目标资源的所有
requests.patch(url, data=None, **kwargs)               #PATCH方法用于对资源应用部分修改
requsets.delete(url, **kwargs)                         #DELETE删除指定的资源
requests.request(method, url,params=None, data=None, headers=None, cookies=None, files=None,verify=None, cert=None, json=None,**kwargs)
#可以构造上述任意的http方法，上述所有方法都是通过调用request()方法实现的
#构造一个向服务器请求资源的Requset对象，返回一个包含服务器资源的Response对象
r = requests.request('GET','https://10.182.83.14/api/webservice/system/info', verify=False)
print(type(r))
print(type(r.status_code),r.status_code)
print(type(r.encoding),r.encoding)
print(type(r.text),r.text)
print(type(r.url),r.url)
print(type(r.content),r.content)
print(type(r.json()),r.json())
print(type(r.headers),r.headers)
print(type(r.request),r.request)
#输出结果
<class 'requests.models.Response'>
<class 'int'> 200
<class 'str'> UTF-8
<class 'str'> {
	"geo_version":"1.0.210526",
	"version":"V2.0R6",
	.....
	"locale":"zh_CN"
}
<class 'str'> https://10.182.83.14/api/webservice/system/info
<class 'bytes'> b'{\n\t"geo_version":"1.0.210526",\n\t"version":"V2.0R6",\n\t"platform":"SG-6000-ISC6205",\n\t"cpuNum":20,\n\t"clusterSize":1,\n\t"uptime":1640166191000,\n\t"hostname":"b9de88a186",\n\t"rule_version":"1.0",\n\t"zone":"Shanghai",\n\t"vm":false,\n\t"memoryTotal":134633631744,\n\t"sn":"419139989",\n\t"time":1643181292224,\n\t"diskMap":{\n\t\t"sda":5999999057920\n\t},\n\t"lib_dns_version":"2.0.220125",\n\t"lib_malcode_version":"2.0.220125",\n\t"lib_ip_version":"2.0.220125",\n\t"lib_vuln_version":"2.0.201210",\n\t"lib_log_parse_config_version":"1.1.210926",\n\t"ips_version":"2.0.2",\n\t"locale":"zh_CN"\n}'
<class 'dict'> {'geo_version': '1.0.210526', 'version': 'V2.0R6', 'platform': 'SG-6000-ISC6205', 'cpuNum': 20, 'clusterSize': 1, 'uptime': 1640166191000, 'hostname': 'b9de88a186', 'rule_version': '1.0', 'zone': 'Shanghai', 'vm': False, 'memoryTotal': 134633631744, 'sn': '419139989', 'time': 1643181292224, 'diskMap': {'sda': 5999999057920}, 'lib_dns_version': '2.0.220125', 'lib_malcode_version': '2.0.220125', 'lib_ip_version': '2.0.220125', 'lib_vuln_version': '2.0.201210', 'lib_log_parse_config_version': '1.1.210926', 'ips_version': '2.0.2', 'locale': 'zh_CN'}
<class 'requests.structures.CaseInsensitiveDict'> {'Server': 'nginx/1.18.0', 'Date': 'Wed, 26 Jan 2022 07:25:23 GMT', 'Content-Type': 'application/json;charset=UTF-8', 'Content-Length': '557', 'Connection': 'keep-alive', 'X-Content-Type-Options': 'nosniff', 'X-XSS-Protection': '1; mode=block', 'Cache-Control': 'no-cache, no-store, max-age=0, must-revalidate', 'Pragma': 'no-cache', 'Expires': '0', 'Strict-Transport-Security': 'max-age=31536000 ; includeSubDomains', 'X-Frame-Options': 'DENY'}
<class 'requests.models.PreparedRequest'> <PreparedRequest [GET]>

Response对象的属性
r.status_code   HTTP返回的状态码,int
r.encoding      响应内容所使用的编码格式,str
r.text          返回的响应内容,str
r.url           请求的url,str
r.content       返回的二进制响应内容,bytes
r.json()        处理json格式的响应内容,dict
r.headers       被请求的服务器的响应头的内容
r.cookies       会话中携带的cookies信息
r.request       原始的请求中的所有内容，包含如r.request.headers:请求头、r.requset.method:请求方式等

#传递url参数
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


#携带数据的post请求
query = {"camefrom": "http://dms.hillstonenet.com/default/@@index.html",
         "username": "shunyu",
         'password': 'YS@184375.asd'}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
}
r = requests.request("post",url="http://dms.hillstonenet.com/default/ldap/@zopen.ldap:login",data = query,verify=False,headers=headers)
print(r.text)
#输出结果
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="" type="blank">
  <head>
    <title>域用户同步-山石网科研发文档管理系统</title>
    ....
    
#下载二进制文件
r = requests.request("GET",url = "https://static.zhihu.com/heifetz/assets/loginBackgroundImg.2c81e205.png", verify=False)
print(r.content)
with open('xxx.png',"wb") as fp:
    fp.write(r.content)
    
#cookies
r = requests.request("get",url="https://10.182.83.14/api/webservice/validate-code/image?id=1643211126771",verify=False)
my_cookies = r.cookies
data = {"userName":"shunyu","password":"QUFiYjExISE=","validateCode":"aaaa"}
r = requests.request("post",url="https://10.182.83.14/api/webservice/user/login",verify=False,cookies = my_cookies,json = data)
print(r.text)
#输出结果 
{
	"result":{
		"department":"",
		"description":"",
		"generation":1,
		"id":7,
		"lastVisitTime":1643211307538,
		"notifyDate":"",
		"password":"",
		"passwordModificationDate":"",
		"passwordTimeoutStartDate":"2021-11-30",
		"role":"admin",
		"token":"419bec4df14c424c83dc5619f109375b",
		"userName":"shunyu"
	},
	"total":0
}
                         
#文件上传


#会话session()
#会话对象让你能够跨请求保持某些参数,它会在同一个 Session 实例发出的所有请求之间保持 cookie
s = requests.session()
s.request("get",url = "https://10.182.83.15/api/webservice/validate-code/image?id=1642572113587",verify=False )
data = {"userName":"shunyu1","password":"QUFiYjExISE=","validateCode":"aaaa"}
r = s.request("post",url = "https://10.182.83.15/api/webservice/user/login", json=data,verify=False)
print(r.text)
query = {'query': {"conditions":[{"field":"timestamp","value":{"start":1640657534000,"end":1643249534000},"operator":8,"logical":1}]}}
r = s.request("get",url = "https://10.182.83.15/api/webservice/monitor/overview/hotEvents", params=query, verify=False)
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
	"total":0
}

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

#delete使用
s = requests.session()
s.request("get",url = "https://10.182.83.15/api/webservice/validate-code/image?id=1642572113587",verify=False )
data = {"userName":"shunyu2","password":"QUFiYjExISE=","validateCode":"aaaa"}
s.request("post",url = "https://10.182.83.15/api/webservice/user/login", json=data,verify=False)
r = s.request('delete',url = "https://10.182.83.15/api/webservice/asset/server/display",verify=False,json = ["10.126.126.8"])
print(r.status_code)
#输出结果
200

```

