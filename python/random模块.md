# random模块

[random --- 生成伪随机数 — Python 3.10.0 文档](https://docs.python.org/zh-cn/3/library/random.html)

```python
random.random() #生成一个[0,1)的随机小数

random.uniform(a,b) #生成[a,b]之间的随机小数

random.randrange(start,stop[,step])  #  产生[start, stop)之间以setp为步长的随机整数
random.randrange(5)  #产生一个[0,5)之间的随机整数

random.randrange(1,6)  #产生一个[1,6)之间的随机整数
random.randrange(1,6,2) #产生一个[1,6)之间，以2为步长的随机整数 也就是说只有可能是1，3，5

random.randint(a,b) #产生一个[a,b]之间的随机整数

random.getrandbits(k)  #具有k个随机比特位的非负整数

random.choice(seq)   #从seq中随机选择一个元素
random.choice(['asd','sads','456'])
Out[240]: '456'

random.choices(seq,weights=None,k=1) #从seq中随机抽取一个元素，重复k次，返回列表，weight表示权重
random.choices([1,2,3,4,5],weights=[5,4,0,0,1],k=10)
Out[252]: [1, 1, 2, 1, 2, 5, 1, 2, 2, 2]

random.sample(seq,k,count=None)  #从seq中随机抽取k个元素，每次抽取完毕之后不放回
random.sample(["一等奖","二等奖","三等奖",'阳光普照'],10,counts=[1,2,3,1000])
Out[255]: 
['阳光普照',
'阳光普照',
'阳光普照',
'阳光普照',
'阳光普照',
'阳光普照',
'阳光普照',
'阳光普照',
'阳光普照',
'阳光普照']

random.shuffle(seq) #将seq中的元素随机打乱，并在原列表中生效
a = [1, 2, 3, 4, 5, 6]
random.shuffle(a)
print(a)
Out[262]: [5, 3, 1, 4, 6, 2]
```

