# json模块

[json --- JSON 编码和解码器 — Python 3.10.0 文档](https://docs.python.org/zh-cn/3/library/json.html)

```python
json.dumps(obj,skipkeys=False,ensure_ascii=True,indent=None,default=None,sort_keys=False,separators=None) #将对象序列化为json格式的字符串
#如果 skipkeys 是 True （默认为False），那么那些不是基本对象（包括 str, int、float、bool、None）的字典的键会被跳过
json.dumps({(1,2):1})
Traceback (most recent call last):
  File "D:\python\lib\site-packages\IPython\core\interactiveshell.py", line 3444, in run_code
    exec(code_obj, self.user_global_ns, self.user_ns)
  File "<ipython-input-173-5827a8fed438>", line 1, in <module>
    json.dumps({(1,2):1})

TypeError: keys must be str, int, float, bool or None, not tuple

json.dumps({(1,2):1},skipkeys=True)
Out[172]: '{}'

#如果 ensure_ascii 是 True （即默认值），输出保证将所有输入的非 ASCII 字符转义。如果 ensure_ascii 是 false，这些字符会原样输出
json.dumps({"哈哈哈":1},ensure_ascii=True)
Out[175]: '{"\\u54c8\\u54c8\\u54c8": 1}'
json.dumps({"哈哈哈":1},ensure_ascii=False)
Out[176]: '{"哈哈哈": 1}'

#如果 indent 是一个非负整数或者字符串，那么 JSON 数组元素和对象成员会被美化输出为该值指定的缩进等级。 
#如果缩进等级为零、负数或者 ""，则只会添加换行符。
#None (默认值) 选择最紧凑的表达。
#如果 indent 是一个字符串 (比如 "asd")，那个字符串会被用于缩进每一层。 
print(json.dumps({"哈哈哈":1,123:None},ensure_ascii=False,indent = 4))
print('-------------')
print(json.dumps({"哈哈哈":1,123:None},ensure_ascii=False,indent = 0))
print('-------------')
print(json.dumps({"哈哈哈":1,123:None},ensure_ascii=False,indent = "asd"))
print('-------------')
print(json.dumps({"哈哈哈":1,123:None},ensure_ascii=False,indent = None))

{
    "哈哈哈": 1,
    "123": null
}
-------------
{
"哈哈哈": 1,
"123": null
}
-------------
{
asd"哈哈哈": 1,
asd"123": null
}
-------------
{"哈哈哈": 1, "123": null}

#separators=(item_separator, key_separator),item_separator表示元素之间的分隔符，key_separator表示键值之间的分隔符
print(json.dumps({"哈哈哈":1,123:None},ensure_ascii=False,indent = 4,separators = ('|','=')))
{
    "哈哈哈"=1|
    "123"=null
}

#如果 sort_keys 是 True（默认为 False），那么字典的输出会以键的顺序排序
print(json.dumps({"b":1,'a':None},ensure_ascii=False,indent = 4))
{
    "b": 1,
    "a": null
}
print(json.dumps({"b":1,'a':None},ensure_ascii=False,indent = 4,sort_keys=True))
{
    "a": null,
    "b": 1
}

json.dump(obj,fp,skipkeys=False,ensure_ascii=True,indent=None,default=None,sort_keys=False,separators=None) 
#将对象序列化为json格式的字符串并保存在文件中
json.dump({"b":1,'a':None},fp = open('xxx.json','w'),ensure_ascii=False,indent = 4,sort_keys=True)

os.listdir()
Out[192]: ['.idea', '222', '555', 'logmanage', 'systemsetup', 'xxx.json']
with open('xxx.json','r') as f:
    print(f.read())
    
{
    "a": null,
    "b": 1
}

json.loads(str) #将json格式的字符串转换为Python对象
json.loads('["foo", {"bar":["baz", null, 1.0, 2]}]')
Out[194]: ['foo', {'bar': ['baz', None, 1.0, 2]}]

json.load(fp) #将json文件中的数据转换为python对象
json.load(open('xxx.json','r'))
Out[195]: {'a': None, 'b': 1}
```

