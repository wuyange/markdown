参考文档：

http://kaito-kidd.com/2017/02/22/python-magic-methods/

https://pyzh.readthedocs.io/en/latest/python-magic-methods-guide.html

## 构造方法

### \__init__(self, [...])

一个基类如果有 `__init__()` 方法，其所派生的类如果也有 `__init__()` 方法，就必须显式地调用它以确保实例基类部分的正确初始化；例如: `super().__init__([args...]).`

### __new__(cls, [...])

https://www.51cto.com/article/711136.html

`__new__`方法接受的参数虽然也是和`__init__`一样，但`__init__`是在类实例创建之后调用，而 `__new__`方法正是创建这个类实例的方法。

#### 类的实例化过程

一般使用`__init__()`方法初始化一个类的实例，当代码中实例化一个类的时候，第一个调用执行的是`__new__()`方法，当定义的类中没有重新定义`__new__()`方法时候，Python会默认调用该父类的`__new__()`方法来构造该实例，`__new__`方法就是先创建一个空间，然后每次创建一个实例化的对象，然后用开辟的空间存放这个实例化对象

- `__new__` 的第一个参数是 `cls`，而 `__init__` 的第一个参数是 `self`
-  `__new__` 优先于 `__init__` 调用
- `__new__` 返回值是一个实例对象，而 `__init__` 没有任何返回值，只做初始化操作
- `__new__` 由于返回的是一个实例对象，所以它可以给所有实例进行统一的初始化操作

#### 通过`__new__`实现单例模式

单例模式最初的定义出现于《设计模式》：“保证一个类仅有一个实例，并提供一个访问它的全局访问点。”

单例的使用主要是在需要保证全局只有一个实例可以被访问的情况，比如系统日志的输出、操作系统的任务管理器等。

```python
class Singleton(object):
    """单例模式"""
    _instance = None
    def __new__(cls, *args, **kwargs):
        # 判断该类的属性是否为None；对第一个对象没有被创建，我们应该调用父类的方法，为第一个对象分配空间
        # 第一个对象创建完成后_instance就不为空了，后续实例化时都会直接返回该实例
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(cls)
        return cls._instance
    
    
class Singleton(object):
    """单例模式的另一种实现"""
	def __new__(cls,*args,**kwargs):
    if not hasattr(cls,"instance"):
        cls.instance = super(Singleton, cls).__new__(cls)
        return cls.instance
```

##### 单例模式下控制类仅执行一次`__inti__`

```python
class Singleton(object):
    _instance = None
    init_flag = False
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls._instance
    def __init__(self,name,data):
        if Singleton.init_flag:
            return
        self.name = name
        self.data = data
        Solution.init_flag = True
```

#### 多例模式

多个实例对象空间引用地址完全独立，从而保持避免不同请求资源不被占用，将同一个对象请求归为同一个实例。

```python
class Solution:
    # 定义类实例化对象字典，即不同的实例对象对应不同的对象空间地址引用
    _loaded = {}
    def __init__(self,name,data):
        self.name = name
        self.data = data
    def __new__(cls, name,*args):
        client = cls._loaded.get(name, None)
        if not client:
            client = super().__new__(cls)
            cls._loaded[name] = client
        return client
```

### \__del__(self)

在实例将被销毁时调用

如果一个基类具有 `__del__()`方法，则其所派生的类如果也有 `__del__()` 方法，就必须显式地调用它以确保实例基类部分的正确清除。

> 备注: `del x` 并不直接调用 `x.__del__()` --- 前者会将 `x` 的引用计数减一，而后者仅会在 `x` 的引用计数变为零时被调用。

## 访问控制

### \__getattr__(self, name)



### \__setattr__(self, name, value)

通过「.」设置属性或 `setattr(key, value)` 设置属性时调用

### \__delattr__(self, name)

### \__getattribute__(self, name)

### \__dir__(self)

### 类的表示

#### \__repr__(self)

由 [`repr()`](https://docs.python.org/zh-cn/3/library/functions.html#repr) 内置函数调用以输出一个对象的“官方”字符串表示。如果可能，这应类似一个有效的 Python 表达式，能被用来重建具有相同取值的对象（只要有适当的环境）。

如果一个类定义了 [`__repr__()`](https://docs.python.org/zh-cn/3/reference/datamodel.html#object.__repr__) 但未定义 [`__str__()`](https://docs.python.org/zh-cn/3/reference/datamodel.html#object.__str__)，则在需要该类的实例的“非正式”字符串表示时也会使用 [`__repr__()`](https://docs.python.org/zh-cn/3/reference/datamodel.html#object.__repr__)。

#### \__str__(self)

通过 [`str(object)`](https://docs.python.org/zh-cn/3/library/stdtypes.html#str) 以及内置函数 [`format()`](https://docs.python.org/zh-cn/3/library/functions.html#format) 和 [`print()`](https://docs.python.org/zh-cn/3/library/functions.html#print) 调用以生成一个对象的“非正式”或格式良好的字符串表示。返回值必须为一个 [字符串](https://docs.python.org/zh-cn/3/library/stdtypes.html#textseq) 对象。

此方法与 [`object.__repr__()`](https://docs.python.org/zh-cn/3/reference/datamodel.html#object.__repr__) 的不同点在于 [`__str__()`](https://docs.python.org/zh-cn/3/reference/datamodel.html#object.__str__) 并不预期返回一个有效的 Python 表达式：可以使用更方便或更准确的描述信息。

- `__str__` 强调可读性，而 `__repr__` 强调准确性 / 标准性
- `__str__` 的目标人群是用户，而 `__repr__` 的目标人群是机器，`__repr__` 返回的结果是可执行的，通过 `eval(repr(obj))` 可以正确运行
- 占位符 `%s` 调用的是 `__str__`，而 `%r` 调用的是 `__repr__` 方法

- 如果只定义了 `_str__`，那么 `repr(person)` 输出 `<__main__.Person object at 0x10bee9390>`
- 如果只定义了 `__repr__`，那么 `str(person)` 与 `repr(person)` 结果是相同的

#### \__bytes__(self)

通过 [bytes](https://docs.python.org/zh-cn/3/library/functions.html#func-bytes) 调用以生成一个对象的字节串表示。这应该返回一个 [`bytes`](https://docs.python.org/zh-cn/3/library/stdtypes.html#bytes) 对象。

#### \__format__(self, format_spec)

通过 [`format()`](https://docs.python.org/zh-cn/3/library/functions.html#format) 内置函数、扩展、[格式化字符串字面值](https://docs.python.org/zh-cn/3/reference/lexical_analysis.html#f-strings) 的求值以及 [`str.format()`](https://docs.python.org/zh-cn/3/library/stdtypes.html#str.format) 方法调用以生成一个对象的“格式化”字符串表示。 *format_spec* 参数为包含所需格式选项描述的字符串。 *format_spec* 参数的解读是由实现 [`__format__()`](https://docs.python.org/zh-cn/3/reference/datamodel.html#object.__format__) 的类型决定的，不过大多数类或是将格式化委托给某个内置类型，或是使用相似的格式化选项语法。







字符串表示:  `__repr__` `__str__`

集合、序列相关:  `__len__` `__getitem__` `__setitem__` `__delitem__` `__contains__`

迭代相关 `__iter__` `__next__`

可调用 `__call__`

with上下文管理器 `__enter__` `__exit__`

数值转换:  `__abs__` `__bool__` `__int__` `__float__` `__hash__` `__index__`

属性相关:  `__getattr__` `__setattr__` `__getattribute__` `__setattribute__` `__dir__`

属性描述符:  `__get__` `__set__` `__delete__`

https://learnku.com/articles/52783

https://docs.python.org/zh-cn/3/howto/descriptor.html#primer

协程:  `__await__` `__aiter__` `__anext__` `__aenter__` `__aexit__`



**「数学运算」**

一元运算符: `__neg__（-）` `__pos__（+）` `__abs__`

二元运算符: `__lt__(<)` `__le__ <=`  `__eq__ ==`  `__ne__ !=`  `__gt__ >`  `__ge__ >=`

算术运算符:  `__add__ +`  `__sub__ -`  `__mul__ *`  `__truediv__ /`  `__floordiv__ //`  `__mod__ %`  `__divmod__ divmod()`  `__pow__ ** 或 pow()`  `__round__ round()`

反向算术运算符: `__radd__`  `__rsub__`  `__rmul__`  `__rtruediv__`  `__rfloordiv__`  `__rmod__` `__rdivmod__`  `__rpow__`

增量赋值算术运算符:`__iadd__`  `__isub__`  `__imul__`  `__itruediv__`  `__ifloordiv__`  `__imod__` `__ipow__`

位运算符: `__invert__ ~`  `__lshift__ <<`  `__rshift__ >>`  `__and__ &`  `__or__ |`  `__xor__ ^`

反向位运算符: `__rlshift__`  `__rrshift__`  `__rand__`  `__rxor__`  `__ror__`

增量赋值位运算符: `__ilshift__`  `__irshift__`  `__iand__`  `__ixor__`  `__ior__`

##  