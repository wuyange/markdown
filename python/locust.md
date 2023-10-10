# locust

## locust简介与安装

### 简介


`Locust`是一个`Python`编写的开源的负载测试工具，可以模拟大量用户同时访问一个`web`应用，从而测试其性能和稳定性。

**Locust有以下特点：**

- 简单易用：`Locust`使用`Python`语言编写，用户可以通过编写`Python`代码来描述测试场景，非常灵活。
- 分布式架构：`Locust`可以部署到多台计算机上，实现高并发访问。
- 实时监控：`Locust`提供了`Web`界面，可以实时查看测试数据和统计结果。
- 可扩展性：`Locust`的代码开源，用户可以根据自己的需要进行二次开发。

### 安装locust

```powershell
pip install locust -i http://pypi.douban.com/simple --trusted-host pypi.douban.com
```



## 运行locust

`Locust`是一个用`Python`编写的程序，它可以对要测试的系统发出请求，下面的脚本会反复发送HTTP请求到"/api/webservice/system/info"

```python
# test.py
from locust import HttpUser, task, constant
# warnings的作用是忽略告警
import warnings
warnings.filterwarnings("ignore")

class RegularUser(HttpUser):
    wait_time = constant(1)
    
    @task
    def hello_world(self):
        self.client.verify = False # 不校验HTTPS的证书
        self.client.get("/api/webservice/system/info")
```

### 通过web页面操作
通过`locust --locustfile test.py` 执行脚本

```shell
(locust) root@master:~/study_locust# locust --locustfile test.py
[2023-05-24 18:35:40,214] master/WARNING/locust.main: System open file limit '1024' is below minimum setting '10000'.
It's not high enough for load testing, and the OS didn't allow locust to increase it by itself.
See https://github.com/locustio/locust/wiki/Installation#increasing-maximum-number-of-open-files-limit for more info.
[2023-05-24 18:35:40,214] master/INFO/locust.main: Starting web interface at http://0.0.0.0:8089 (accepting connections from all network interfaces)
[2023-05-24 18:35:40,232] master/INFO/locust.main: Starting Locust 2.15.1
```
> **性能测试相关概念**
>
> 1.**在线用户**，表示某个时间段内在服务器上保持登录状态的用户。但在线用户不一定是对服务器产生压力的用户，只有正在操作的活跃用户才会对服务器产生压力，在线只是一种状态。
> 2.**相对并发用户**，类似活跃用户，表示某个时间段内与服务器保持交互的用户，理论上这些用户有同一时刻 (即绝对并发进行操作的可能(对这种可能性的度量称为并发度)。相对并发的说法主要是为了区分绝对并发。
> 3.**绝对并发用户**，表示同一时间点(严格地说是足够短的时间段内)与服务器进行交互的用户。
> 4.**思考时间**，表示用户每个操作后的暂停时间，或者叫作操作之间的间隔时间，此时间内用户是不对服务器产生压力的。如果想了解系统在极端情况下的性能表现，可以设置思考时间为0;而如果要预估系统能够承受的最大压力，就应该尽可能地模拟真实思考时间。
> 5.**响应时间**，通常包括网络传输请求的时间、服务器处理的时间，以及网络传输响应的时间。而我们重点关心的应该是服务器处理的时间，这部分受到代码处理请求的业务逻辑的影响，从中可以真正发现缺陷并对业务逻辑进行优化而网络传输请求和响应的时间很大程度上取决于网络质量。
> 6.**RPS**，指每秒处理的请求数，是直接反映系统性能的指标


### 通过命令行操作
```shell
locust --locustfile script.py --headless --users 10000 --spawn-rate 10 -H https://10.182.83.191
# script.py 脚本名称
# --headless 不支持UI
# --users 10000 设置用户最大数量为10000
# --spawn-rate 10 设置用户增长速度为10
# -H 设置被测试的主机
```


## 编写locustfile

现在来看一个完整的例子

```python
import warnings
warnings.filterwarnings("ignore")
from locust import HttpUser, task, between
import base64


# 用户列表
num = 0
user_list = [{'userName': 'locust_user1', 'password': 'AAbb11!!'}, 
             {'userName': 'locust_user2', 'password': 'AAbb11!!'},
             {'userName': 'locust_user3', 'password': 'AAbb11!!'},
             {'userName': 'locust_user4', 'password': 'AAbb11!!'},
             {'userName': 'locust_user5', 'password': 'AAbb11!!'}]

def decryption(s, encoding='utf-8'):
    return base64.b64encode(s.encode(encoding=encoding)).decode(encoding=encoding)

class QuickstartUser(HttpUser):
    wait_time = between(1,5)

    @task(2)
    def chk_asset_list(self):
        # 获取资产列表
        for i in range(10):
            query = '{"start":0,"limit":' + str(i) + ',"conditions":[{"field":"networkId","value":[1],"operator":7,"logical":1}]}'
            r = self.client.get(f"/api/webservice/asset/management?query={query}", name="/management")
            print(r.text)
        
    @task(2)
    def chk_os_distribution(self):
        # 获取操作系统分布
        r = self.client.get("/api/webservice/asset/os",)
        print(r.text)
        
    @task(1)
    def chk_info(self):
        # 获取智源信息
        r = self.client.get("/api/webservice/system/info",)
        print(r.text)

    def on_start(self):
        data = user_list[num % 5]
        data['password'] = decryption(data['password'])
        # 设置无需验证证书
        self.client.verify = False
        # 登录
        r = self.client.post("/api/webservice/user/sso/login", data=data)
        print(r.request)
        
    def on_stop(self):
        # 退出登录
        r = self.client.post("/api/webservice/user/logout")
        print(r.request)
```



```python
class QuickstartUser(HttpUser):
```

在这里，我们定义了一个用于模拟的用户类。它继承自`HttpUser`类，为每个用户提供了一个`client`属性，该属性是`HttpSession`的一个实例，可用于向目标系统发起负载测试的HTTP请求。当测试开始时，`Locust`将为每个模拟的用户创建此类的一个实例，并且每个用户将在自己的绿色`gevent`线程中开始运行。

>在`Python`中，线程通常是由操作系统进行调度的，每个线程都需要占用一定的内存和系统资源。与之相比，协程是一种用户态的轻量级线程，它由程序员在代码中显式地进行控制，而不需要操作系统进行调度。
>
>`gevent`是一个基于`libev`或`libuv`的`Python`网络库，它实现了绿色线程的概念。通过使用`gevent`，可以在单个线程中运行多个绿色`gevent`线程，这些线程可以在遇到网络IO或其他阻塞操作时自动切换，从而充分利用CPU资源，并提高并发性能。

```python
wait_time = between(1, 5)
```

`QuickstartUser`类定义了一个`wait_time`属性，这将使模拟的用户在执行完每个任务后等待1到5秒钟的时间间隔。

```python
@task
def chk_asset_type_distribution(self):
    ...
```

用`@task`装饰的方法是`Locustfile`的核心内容。对于每个正在运行的用户，`Locust`会创建一个绿色线程（微线程），并调用这些方法。

```python
@task(2)
def chk_asset_list(self):
    # 获取资产列表
    for i in range(10):
        query = '{"start":0,"limit":' + str(i) + ',"conditions":[{"field":"networkId","value":[1],"operator":7,"logical":1}]}'
        r = self.client.get(f"/api/webservice/asset/management?query={query}", name="/management")
        print(r.text)
    
@task(2)
def chk_os_distribution(self):
    # 获取操作系统分布
    r = self.client.get("/api/webservice/asset/os",)
    print(r.text)
    
@task(1)
def chk_info(self):
    # 获取智源信息
    r = self.client.get("/api/webservice/system/info",)
    print(r.text)
...
```

通过在三个方法上使用`@task`装饰器定义了三个任务，当`QuickstartUser`运行时，它会随机的选择上述三个任务中的一个执行，但他们被选中的概率是不一致的。上面的配置`Locust`选择`chk_os_distribution`和`chk_asset_list`的几率是选择`chk_info`的2倍。当任务执行完成后，用户将在其等待时间（在这种情况下为1到5秒）内休眠。在等待时间之后，用户将选择新任务并重复执行。 

>只有用`@task`装饰的方法才会被选中，因此可以按照自己的喜好定义自己的内部辅助方法。

```
self.client.get("/hello")
```

`self.client`属性使得在`Locust`中可以进行`HTTP`调用，并且这些调用会被`Locust`记录。

```python
@task(2)
def chk_asset_list(self):
    # 获取资产列表
    for i in range(10):
        query = '{"start":0,"limit":' + str(i) + ',"conditions":[{"field":"networkId","value":[1],"operator":7,"logical":1}]}'
        r = self.client.get(f"/api/webservice/asset/management?query={query}", name="/management")
        print(r.text)
```

在`chk_asset_list`任务中，通过使用一个可变的查询参数加载10个不同的URL。为了不在`Locust`的统计数据中得到10个单独的条目（因为统计数据是按`URL`分组的），我们使用了`name`参数，将所有这些请求都分组在名为`"/api/webservice/asset/management"`的条目下。

```python
def on_start(self):
    data = user_list[num % 5]
    data['password'] = decryption(data['password'])
    # 设置无需验证证书
    self.client.verify = False
    # 登录
    r = self.client.post("/api/webservice/user/sso/login", data=data)
    print(r.request)
    
def on_stop(self):
    # 退出登录
    r = self.client.post("/api/webservice/user/logout")
    print(r.request)
```

每个模拟用户在开始运行时，都会调用这个名为`on_start`的方法。在`Locust`中，`on_start`方法允许我们在每个模拟用户开始运行之前进行一些初始化操作，例如登录、准备测试数据等。



## User class

`Locust`中的用户类（`User class`）代表了您系统中的一个用户类型或场景。在进行测试运行时，您需要指定要模拟的并发用户数量，`Locust`将为每个用户创建一个用户类的实例。您可以为这些类/实例添加任何您喜欢的属性，但有一些属性对Locust有特殊的意义。

### wait_time属性

用户的`wait_time`方法可以轻松地在每个任务执行后引入延迟。如果没有指定`wait_time`，则下一个任务将在上一个任务完成后立即执行。

```python
from locust import User, task, between, constant, constant_pacing, constant_throughput

class MyUser(User):
    @task
    def my_task(self):
        print("executing my_task")
	
    # 每个任务之间间隔0.5~10s
    wait_time = between(0.5, 10)
    # 每个任务之间固定间隔5s
    wait_time = constant(5)
    # 每个任务的开始时间间隔10秒
    wait_time = constant_pacing(10)
    # 每秒运行1个任务
    wait_time = constant_throughput(1)
```

- `constant`：表示固定的等待时间，用户每个任务执行后都会等待相同的时间。
- `between`：表示在最小值和最大值之间的随机等待时间，用户每个任务执行后会等待一个随机的时间。
- `constant_throughput`：表示以恒定的吞吐量运行任务的适应性等待时间。它会根据目标吞吐量限制任务的执行频率，确保每秒钟最多运行X次任务。
- `constant_pacing`：表示以恒定的节奏运行任务的适应性等待时间。它会根据目标节奏限制任务的执行频率，确保任务每隔X秒运行一次（它是`constant_throughput`的数学倒数）。

#### 自定义wait_time

也可以直接在类上声明自己的`wait_time`方法。例如，以下`User`类将休眠一秒钟，然后是两秒钟，然后是三秒钟，依此类推。

```python
class MyUser(User):
    last_wait_time = 0

    def wait_time(self):
        self.last_wait_time += 1
        return self.last_wait_time
```

### weight和fixed_count属性

如果文件中存在多个用户类，并且命令行上未指定用户类，则`Locust`将生成相同数量的每个用户类。还可以通过将它们作为命令行参数传递来指定从同一`locustfile`使用哪些用户类

```shell
# locust -f locust_file.py WebUser MobileUser
locust -f locust_file.py AdministratorUser AuditorUser OnlyReadUser
```

如果希望模拟某种类型的更多用户，则可以在这些类上设置权重属性。例如，管理员用户的可能性是日志审计员的三倍：

```python
class AdministratorUser(User):
    weight = 3
    ...

class OnlyReadUser(User):
    weight = 1
    ...
```

也可以设置属性`fixed_count`。在这种情况下，权重属性将被忽略，并将生成确切的计数用户，首先生成这些用户。
在下面的示例中，只会生成一个`AuditorUser`实例，以便进行一些特定的工作，独立于用户总数更准确地控制请求计数。

```python
class AuditorUser(User):
    wait_time = constant(600)
    fixed_count = 1

    @task
    def chk_log(self):
        ...

class AdministratorUser(User):
    ...
```

### on_start和on_stop方法

`Users`（以及`TaskSets`）可以定定义`on_start`方法和`on_stop`方法。当用户开始运行时，用户将调用其`on_start`方法；当用户停止运行时，用户将调用其`on_stop`方法。
对于任务集，当模拟用户开始执行该任务集时，将调用`on_start`方法，当模拟用户停止执行该任务集时（当调用`interrupt()`或用户被终止时），将调用`on_stop`方法。

## HttpUser class

`HttpUser`是最常用的`User`。它添加一个用于发出`HTTP`请求`client`的属性。

```python
from locust import HttpUser, task, between

class MyUser(HttpUser):
    wait_time = between(5, 15)

    @task(4)
    def index(self):
        self.client.get("/")

    @task(1)
    def about(self):
        self.client.get("/about/")
```

### client attribute / HttpSession

`client`是 `HttpSession`的实例。`HttpSession`是`requests.Session` 的子类/包装器，因此它的功能有很好的文档记录，并且应该为许多人所熟悉。`HttpSession`添加的主要是将请求结果报告到`Locust`中（成功/失败、响应时间、响应长度、名称）。

它包含所有`HTTP`方法的方法：`get`、`post`、`put` 、...。就像`requests.Session`一样，它在请求之间保留`cookie`，因此可以轻松用于登录网站。

```python
response = self.client.post("/login", {"username":"testuser", "password":"secret"})
print("Response status code:", response.status_code)
print("Response text:", response.text)
response = self.client.get("/my-profile")
```

可以通过使用`catch_response`参数、`with`语句和`response.failure()`将请求标记为失败。

```python
with self.client.get("/", catch_response=True) as response:
    if response.text != "Success":
        response.failure("Got wrong response")
    elif response.elapsed.total_seconds() > 0.5:
        response.failure("Request took too long")
```

还可以将请求标记为成功，即使响应代码错误：

```python
with self.client.get("/does_not_exist/", catch_response=True) as response:
    if response.status_code == 404:
        response.success()
```

### 分组请求

网站的网页网址包含某种动态参数是很常见的。通常，在用户的统计信息中将这些`URL`组合在一起是有意义的。这可以通过将`name`参数传递给 `HttpSession's` 不同的请求方法来完成。

```python
# Statistics for these requests will be grouped under: /blog/?id=[id]
for i in range(10):
    self.client.get("/blog?id=%i" % i, name="/blog?id=[id]")
```

## Tasks

开始测试时，将为每个模拟用户创建一个`User`类的实例，这些用户将开始在自己的绿色线程中运行。
当这些用户运行时，他们选择他们执行的任务，休眠一段时间，然后选择一个新任务，依此类推。

### @task装饰器

为用户添加任务的最简单方法是使用`task`修饰器。

```python
from locust import User, task, constant

class MyUser(User):
    wait_time = constant(1)

    @task
    def my_task(self):
        print("User instance (%r) executing my_task" % self)
```

`@task`可以于指定任务执行的权重。在以下示例中，选择`task2`的可能性是`task1`的两倍：

```python
from locust import User, task, between

class MyUser(User):
    wait_time = between(5, 15)

    @task(3)
    def task1(self):
        pass

    @task(6)
    def task2(self):
        pass
```

### tasks属性

定义用户任务的另一种方法是设置`tasks`属性

`tasks`属性是`Tasks`列表或`字典`，其中`Task`是`python`可调用对象或`TaskSet`类。如果任务是普通的`python`函数，它们会收到一个参数，即执行任务的用户实例。

下面是一个声明为普通 python 函数的用户任务的示例：

```python
from locust import User, constant

def chk_info(self):
    self.client.verify = False
    self.client.get("/api/webservice/system/info")

class MyUser(User):
    tasks = [chk_info]
    wait_time = constant(1)
```

将任务属性指定为列表或者字典，以下两种方式都表示执行`my_task`的概率是`another_task`的三倍

```python
tasks = [my_task, my_task, my_task, another_task]
tasks = {my_task: 3, another_task: 1}
```
> **缺点**：使用`tasks`需要保证函数已经定义

### @tag装饰器

通过使用装饰器标记`@tag`任务，可以使用`--tags`和`--exclude-tags`参数决定脚本会执行哪些任务。

```python
from locust import User, constant, task, tag

class MyUser(User):
    wait_time = constant(1)

    @tag('tag1')
    @task
    def task1(self):
        print('-----------task1---------')

    @tag('tag1', 'tag2')
    @task
    def task2(self):
        print('-----------task2---------')

    @tag('tag3')
    @task
    def task3(self):
        print('-----------task3---------')

    @task
    def task4(self):
        print('-----------task4---------')
```

如果使用`--tags tag1`，则在测试期间将仅执行`task1`和`task2`。如果使用`--tags tag2 tag3`它，则只会执行`task2`和`task3`。

`--exclude-tags`将以完全相反的方式行事。因此，如果使用`--exclude-tags tag3`测试，则只会执行`task1 task2 task4`。

如果`--exclude-tags`和`--tags`中的内容有冲突，则以`--exclude-tags`为准


## TaskSet class

`TaskSet` 是一种组织用户行为的方式。它允许将一组相关的任务（或行为）组织在一起，以便更好地管理和模拟用户的行为流。

```python
from locust import User, TaskSet, constant

class TestAsset(TaskSet):
    wait_time = constant(1)

    @task(10)
    def new_asset(self):
        pass

    @task
    def new_service(self):
        pass

    @task
    def new_area(self):
        pass

class AdministratorUser(User):
    wait_time = constant(5)
    tasks = {TestAsset:2}

    @task
    def my_task(self):
        pass
```

`Taskset`和`User`类中都定义了`wait_time`时，以`Taskset`为准

任务集永远不会停止执行任务，并将执行移交给父用户/任务集。这必须由开发人员通过调用 `TaskSet.interrupt()`方法来完成
如果`reschedule`参数设置为`True`（默认值），则任务将被重新安排，并在后续的任务队列中重新执行。这意味着任务将在稍后再次执行，直到达到指定的条件或计数为止。
如果`reschedule`参数设置为`False`，则任务将被中断，但不会重新安排。这意味着任务将被完全取消，不会再次执行。

通过使用`TaskSet`，可以更有效地组织和管理用户的行为，使代码更加结构化和可扩展。

`TaskSet`类的任务可以是其他`TaskSet`类，允许它们嵌套任意数量的级别。能够定义一种以更真实的方式模拟用户的行为。

例如，我们可以使用以下结构定义任务集：

```
- Main user behaviour
  - Asset page
  - Risk page
  - Threat categories
```

### SequentialTaskSet

`SequentialTaskSet`是一个任务集，其任务将按声明顺序执行。

```python
from locust import User, constant, task, tag, TaskSet,SequentialTaskSet

class MyUser(User):
    wait_time = constant(1)
    
    @task
    class SequenceOfTasks(SequentialTaskSet):
        wait_time = constant(1)

        @task
        def task1(self):
            print('-----------task1---------')
            
        @task  
        def task2(self):
            print('-----------task2---------')
            
        @task    
        def task3(self):
            print('-----------task3---------')
```

以上代码将按顺序执行task1 task2 task3

```python
from locust import User, constant, task, tag, TaskSet,SequentialTaskSet

class MyUser(User):
    wait_time = constant(1)
    
    @task
    class SequenceOfTasks(SequentialTaskSet):
        wait_time = constant(1)

        @task(1)
        def task1(self):
            print('-----------task1---------')
            
        @task(2)
        def task2(self):
            print('-----------task2---------')
            
        @task(3)  
        def task3(self):
            print('-----------task3---------')
```

以上代码将按顺序执行task1 task2 task2 task3 task3 task3

## 实战演练
```python
from locust import HttpUser, task, between, TaskSet, SequentialTaskSet, constant
from faker import Faker
import base64
import hashlib
import uuid
import pymysql
from random import choice, sample, randint
import warnings
warnings.filterwarnings("ignore")

fake = Faker(locale='zh_CN')


class CreateUser(object):
    
    all_user_list = []
    
    def __init__(self, user_type:str, user_num:int):
        role_mapping = {'系统管理员': 'admin', 
                        '系统操作员':'operator', 
                        '日志审计员':'audit',
                        '系统操作员(只读)':'readonly'}
        self.user_type = role_mapping[user_type]
        self.user_num = user_num if user_num >= 1 else 1
        self.user_list = []
        self.user_index = 0
        # 连接数据库
        self.db = pymysql.connect(host='10.182.28.3', 
                            user='hillstone', 
                            password='hIllstoneBdap4Ever',
                            database='bdap', 
                            charset='utf8')
        self.cursor = self.db.cursor()

    def _encryption(self, cleartext:str, encoding:str='utf'):
        # base64编码 单点登录使用
        base64_password = base64.b64encode(cleartext.encode(encoding=encoding)).decode(encoding=encoding)
        # md5编码 插入数据库使用
        md5_password = hashlib.md5(cleartext.encode('utf-8')).hexdigest().upper()
        password = ''
        for i in md5_password:
            if i.isdigit():
                password += str((int(i) + 1) % 10)
            else:
                password += i
        return base64_password, password
    
    def create_user(self):
        for _ in range(self.user_num):
            # 避免名称重复
            name = fake.name()
            while name in CreateUser.all_user_list:
                name = fake.name()
            CreateUser.all_user_list.append(name)
            base64_passwd, passwd = self._encryption(fake.password(length=10, special_chars=True, digits=True, upper_case=True, lower_case=True))
            sql = f'insert into admin_manage(generation, password, role, userName) values(1, "{passwd}", "{self.user_type}", "{name}");'
            self.cursor.execute(sql)
            self.user_list.append({'userName': name, 'password': base64_passwd})
        self.db.commit()
        print(f'创建{self.user_num}个{self.user_type}完成')
        
    def get_user(self):
        user = self.user_list[self.user_index]
        self.user_index = (self.user_index + 1) % self.user_num
        return user
    
    def __del__(self):
        for user in self.user_list:
            sql = f'delete from admin_manage where userName="{user["userName"]}";'
            self.cursor.execute(sql)
            CreateUser.all_user_list.remove(user["userName"])
        self.db.commit()
        self.db.close()
        print(f'删除{self.user_num}个{self.user_type}完成')

class NewArea(TaskSet):
    wait_time = constant(1)
    
    @task
    def new_area(self):
        res = self.client.get("/api/webservice/asset/region/list", 
                            params = 'query={"start":0,"limit":1}', 
                            name="/api/webservice/asset/region/list")
        if res.json()['total'] < 900:
            name = fake.country()
            data = {"name":name,"geo":[name],"priority":0}
            with self.client.post("/api/webservice/asset/region", json=data, catch_response=True) as response:
                if response.status_code != 200 and response.json()['code'] in (8009, 8018):
                    response.success()
                elif response.status_code != 200:
                    print(response.text)
    
    @task(2)
    def exit(self):
        self.interrupt()

class NewService(TaskSet):
    
    wait_time = constant(1)
    
    @task
    def new_service(self):
        res = self.client.get("/api/webservice/asset/business", 
                            params = 'query={"start":0,"limit":1}', 
                            name="/api/webservice/asset/business")
        if res.json()['total'] < 150:
            name = fake.job() 
            data = {"name":name,"priority":0}
            with self.client.post("/api/webservice/asset/business", json=data, catch_response=True) as response:
                if response.status_code != 200 and response.json()['code'] == 8009:
                    response.success()
                elif response.status_code != 200:
                    print(response.text)
                
            
    @task(2)
    def exit(self):
        self.interrupt()

class NewAsset(SequentialTaskSet):
    
    wait_time = between(1, 5)
    tasks = [NewArea,NewService]
    
    def get_service_id(self):
        res = self.client.get("/api/webservice/asset/business", 
                            params = 'query={"start":0,"limit":200}', 
                            name="/api/webservice/asset/business")
        return sample([_['id'] for _ in res.json()['result']], k=randint(1,5))
    
    def get_area_id(self):
        res = self.client.get("/api/webservice/asset/region/list", 
                            params = 'query={"start":0,"limit":1000}', 
                            name="/api/webservice/asset/region/list")
        return choice([_['id'] for _ in res.json()['result']])
    
    @task(5)
    def new_asset(self):
        ip = fake.ipv4()
        region_id = self.get_area_id()
        service_id = self.get_service_id()
        mac = fake.mac_address()
        name = str(uuid.uuid4())
        os_names = choice(["Linux", "Windows", "macOS", "Unix", "FreeBSD"])
        data = {"force":False,
                "data":{"name":name,"ip":[ip],"assetType":1,
                        "regionId":region_id,"mac":[mac],
                        "businessIds":service_id,
                        "priority":0,"extraType":11,
                        "ports":[],"networkId":1,
                        "os":os_names}}
        with self.client.post('/api/webservice/asset/management', json=data, catch_response=True) as response:
            if response.status_code != 200 and response.json()['code'] == 24006:
                response.success()
            elif response.status_code != 200:
                print(response.text)
    
    @task
    def exit(self):
        self.interrupt()
        
class CheckLog(TaskSet):
    
    wait_time = between(1,5)
    
    @task(20)
    def check_event_log(self):
        query = 'query={"start":0,"limit":20,"conditions":[{"field":"type","value":"event","operator":1,"logical":1}],"sorts":[{"field":"timestamp","order":"desc"}]}'
        self.client.get("/api/webservice/systemlog/log", params = query, 
                        name="/api/webservice/asset/systemlog/log")
        
    @task(20)
    def check_operator_log(self):
        query = 'query={"start":0,"limit":20,"conditions":[{"field":"type","value":"operation","operator":1,"logical":1}],"sorts":[{"field":"timestamp","order":"desc"}]}'
        self.client.get("/api/webservice/systemlog/log", params = query, 
                        name="/api/webservice/asset/systemlog/log")
        
    @task
    def exit(self):
        self.interrupt()

class CheckSituationMonitor(TaskSet):
    
    wait_time = between(1,20)
    
    @task
    def check_overall_security_situation_monitor(self):
        with self.client.put("/api/webservice/cache/clear", json = {"platform":[-1]}, catch_response=True) as response:
            if response.status_code != 200 and response.json()['code'] == '403':
                response.success()
        query = 'query={"platform":[-1],"conditions":[{"field":"timestamp","value":{"start":1694080501214,"end":1694685301214},"operator":8,"logical":1}],"queryCacheInterval":"7d"}'
        self.client.get("/api/webservice/risk/overview/score", params = query, 
                        name="/api/webservice/risk/overview/score")
        query = 'query={"start":0,"limit":20,"platform":[-1],"conditions":[{"field":"timestamp","value":{"start":1694080501222,"end":1694685301222},"operator":8,"logical":1}],"queryCacheInterval":"7d"}'
        self.client.get("/api/webservice/risk/server/severity/statistics", params = query, 
                        name="/api/webservice/risk/server/severity/statistics")
        query = 'query={"platform":[-1],"conditions":[{"field":"timestamp","value":{"start":1694489288313,"end":1695094088313},"operator":8,"logical":1}],"queryCacheInterval":"7d"}'
        self.client.get("/api/webservice/fullscreen/overview/threat", params = query, 
                        name="/api/webservice/fullscreen/overview/threat")
        query = 'query={"platform":[-1],"conditions":[{"field":"timestamp","value":{"start":1692517268841,"end":1695109268841},"operator":8,"logical":1}],"queryCacheInterval":"30d"}'
        self.client.get("/api/webservice/risk/terminal/severity/top/5", params = query, 
                        name="/api/webservice/risk/terminal/severity/top/5")
        
    @task
    def check_external_attack_situation_monitor(self):
        with self.client.put("/api/webservice/cache/clear", json = {"platform":[-1]}, catch_response=True) as response:
            if response.status_code != 200 and response.json()['code'] == '403':
                response.success()
        query = 'query={"platform":[-1],"conditions":[{"field":"timestamp","value":{"start":1694080884401,"end":1694685684401},"operator":8,"logical":1}],"queryCacheInterval":"7d"}'
        self.client.get("/api/webservice/fullscreen/outward/situation/earth", params = query, 
                        name="/api/webservice/fullscreen/outward/situation/earth")
        query = 'query={"platform":[-1],"conditions":[{"field":"timestamp","value":{"start":1694080884403,"end":1694685684403},"operator":8,"logical":1}],"queryCacheInterval":"7d"}'
        self.client.get("/api/webservice/fullscreen/outward/situation/asset/Top5", params = query, 
                        name="/api/webservice/fullscreen/outward/situation/asset/Top5")
        query = 'query={"platform":[-1],"conditions":[{"field":"timestamp","value":{"start":1694080884404,"end":1694685684404},"operator":8,"logical":1}],"queryCacheInterval":"7d"}'
        self.client.get("/api/webservice/fullscreen/outward/situation/region/Top5", params = query, 
                        name="/api/webservice/fullscreen/outward/situation/region/Top5")

class CheckRiskPage(TaskSet):
    
    @task
    def check_risk_asset_list(self):
        query = 'query={"start":0,"limit":20,"platform":[-1],"conditions":[{"field":"timestamp","value":{"start":1694504608000,"end":1695109408000},"operator":8,"logical":1}],"sorts":[{"field":"severity","order":"desc"}]}'
        self.client.get("/api/webservice/risk/asset/list", params = query, 
                        name="/api/webservice/risk/asset/list")
       
    @task 
    def check_risk_service_list(self):
        query = 'query={"start":0,"limit":20,"platform":[-1],"conditions":[{"field":"timestamp","value":{"start":1692517586000,"end":1695109586000},"operator":8,"logical":1}],"sorts":[{"field":"severity","order":"desc"}]}'
        self.client.get("/api/webservice/risk/business/list", params = query, 
                        name="/api/webservice/risk/business/list")

class BaseUser(HttpUser):
    
    def create_user(self):
        self.user = CreateUser(self.user_type, self.user_num)
        self.user.create_user()
    
    def on_start(self):
        data = self.user.get_user()
        # 设置无需验证证书
        self.client.verify = False
        # 登录
        response = self.client.post("/api/webservice/user/sso/login", data=data)
        if response.status_code == 200:
            print(f'用户:{data["userName"]}登录成功, 角色为{self.user_type}')
        else:
            print(response.text)
            print(f'用户:{data["userName"]}登录失败, 角色为{self.user_type}')
        
    def on_stop(self):
        # 退出登录
        self.client.post("/api/webservice/user/logout")
        del self.user
    
class AdministratorUser(BaseUser):
    
    wait_time = between(1, 10)
    weight = 2
    tasks = {NewAsset:3, CheckLog:1, CheckRiskPage:1}
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_type = '系统管理员'
        self.user_num = 1
        self.create_user()
        
class ReadOnlyUser(BaseUser):
    
    weight = 10
    tasks = {CheckSituationMonitor: 3, CheckRiskPage:1}
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_type = '系统操作员(只读)'
        self.user_num = 1
        self.create_user()     

class AuditorUser(BaseUser):
    
    fixed_count = 1
    tasks = [CheckLog]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_type = '日志审计员'
        self.user_num = 1
        self.create_user()  


```
