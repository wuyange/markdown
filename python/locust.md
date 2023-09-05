# locust

## locust简介与安装

### 简介


Locust 是一个 Python 编写的开源的负载测试工具，可以模拟大量用户同时访问一个 web 应用，从而测试其性能和稳定性。Locust 采用分布式架构，支持使用多台计算机模拟高并发访问，可以实现千万级别的并发模拟。

**Locust 有以下特点：**

- 简单易用：Locust 使用 Python 语言编写，用户可以通过编写 Python 代码来描述测试场景，非常灵活。
- 分布式架构：Locust 可以部署到多台计算机上，实现高并发访问。
- 实时监控：Locust 提供了 Web 界面，可以实时查看测试数据和统计结果。
- 可扩展性：Locust 的代码开源，用户可以根据自己的需要进行二次开发。

**Locust 的工作流程如下**：

- 通过编写 Python 代码描述测试场景，包括用户行为和场景设置。
- 启动 Locust 进程，指定运行参数，包括并发用户数量、每秒请求数等。
- Locust 模拟用户行为，向目标服务器发送请求，记录测试数据。
- Locust 输出测试结果，包括每秒请求数、响应时间、错误率等，用户可以实时监控和分析测试结果。

### 安装locust

```powershell
pip install locust -i http://pypi.douban.com/simple --trusted-host pypi.douban.com
```



## 快速入门

Locust 是一个用 Python 编写的程序，它可以对你想要测试的系统发出请求,这使得它非常灵活，特别适合实现复杂的用户流程。但它也可以进行简单的测试，下面的脚本会会反复发送HTTP请求到"/api/webservice/system/info"

```python
# test.py
from locust import HttpUser, task
# warnings的作用是忽略告警
import warnings
warnings.filterwarnings("ignore")

class HelloWorldUser(HttpUser):
    @task
    def hello_world(self):
        self.client.verify = False # 不校验HTTPS的证书
        self.client.get("/api/webservice/system/info")
```

### 通过web页面操作

通过`locust --locustfile test.py` 执行脚本名

```shell
(locust) root@master:~/study_locust# locust --locustfile study_1.py
[2023-05-24 18:35:40,214] master/WARNING/locust.main: System open file limit '1024' is below minimum setting '10000'.
It's not high enough for load testing, and the OS didn't allow locust to increase it by itself.
See https://github.com/locustio/locust/wiki/Installation#increasing-maximum-number-of-open-files-limit for more info.
[2023-05-24 18:35:40,214] master/INFO/locust.main: Starting web interface at http://0.0.0.0:8089 (accepting connections from all network interfaces)
[2023-05-24 18:35:40,232] master/INFO/locust.main: Starting Locust 2.15.1

```

### 通过命令行操作

```shell
locust --locustfile script.py --headless --users 10000 --spawn-rate 10 -H https://10.182.83.191
# script.py 脚本名称
# --headless 不支持UI
# --users 10000 设置用户最大数量为10000
# --spawn-rate 10 设置用户增长速度为10
# -H 设置被测试的主机IP
```



## 编写locustfile

现在来看一个完整的例子

```python
import time
from locust import HttpUser, task, between

class QuickstartUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def hello_world(self):
        self.client.get("/hello")
        self.client.get("/world")

    @task(3)
    def view_items(self):
        for item_id in range(10):
            self.client.get(f"/item?id={item_id}", name="/item")
            time.sleep(1)

    def on_start(self):
        self.client.post("/login", json={"username":"foo", "password":"bar"})
```



```python
class QuickstartUser(HttpUser):
```

在这里，我们定义了一个用于模拟的用户类。它继承自`HttpUser`类，为每个用户提供了一个`client`属性，该属性是`HttpSession`的一个实例，可用于向目标系统发起负载测试的HTTP请求。当测试开始时，`Locust`将为每个模拟的用户创建此类的一个实例，并且每个用户将在自己的绿色`gevent`线程中开始运行。

>在Python中，线程通常是由操作系统进行调度的，每个线程都需要占用一定的内存和系统资源。与之相比，协程是一种用户态的轻量级线程，它由程序员在代码中显式地进行控制，而不需要操作系统进行调度。
>
>gevent是一个基于libev或libuv的Python网络库，它实现了绿色线程的概念。通过使用gevent，您可以在单个线程中运行多个绿色gevent线程，这些线程可以在遇到网络IO或其他阻塞操作时自动切换，从而充分利用CPU资源，并提高并发性能。

```python
wait_time = between(1, 5)
```

`QuickstartUser`类定义了一个`wait_time`属性，这将使模拟的用户在执行完每个任务后等待1到5秒钟的时间间隔。

```python
@task
def hello_world(self):
    ...
```

用`@task`装饰的方法是`Locustfile`的核心内容。对于每个正在运行的用户，Locust会创建一个绿色线程（微线程），并调用这些方法。

```python
@task
def hello_world(self):
    self.client.get("/hello")
    self.client.get("/world")

@task(3)
def view_items(self):
...
```

通过在两个方法上使用`@task`装饰器定义了两个任务，其中一个方法的权重设置为3。当`QuickstartUser`运行时，它会选择声明的两个任务中的一个执行，其中`hello_world`和`view_items`两个任务都有可能被执行。任务是随机选择的，但可以给它们不同的权重。上面的配置将使`Locust`选择`view_items`的几率比选择`hello_world`高三倍。当任务执行完成后，用户将在其等待时间（在这种情况下为1到5秒）内休眠。在等待时间之后，用户将选择新任务并重复执行。 

>只有用`@task`装饰的方法才会被选中，因此可以按照自己的喜好定义自己的内部辅助方法。

```
self.client.get("/hello")
```

`self.client`属性使得在`Locust`中可以进行`HTTP`调用，并且这些调用会被`Locust`记录。

```python
@task(3)
def view_items(self):
    for item_id in range(10):
        self.client.get(f"/item?id={item_id}", name="/item")
        time.sleep(1)
```

在`view_items`任务中，我们通过使用一个可变的查询参数加载10个不同的URL。为了不在`Locust`的统计数据中得到10个单独的条目（因为统计数据是按`URL`分组的），我们使用了`name`参数，将所有这些请求都分组在名为`"/item"`的条目下。

```python
def on_start(self):
    self.client.post("/login", json={"username":"foo", "password":"bar"})
```

每个模拟用户在开始运行时，都会调用这个名为`on_start`的方法。在`Locust`中，`on_start`方法允许我们在每个模拟用户开始运行之前进行一些初始化操作，例如登录、准备测试数据等。



## User class

Locust中的用户类（User class）代表了您系统中的一个用户类型或场景。在进行测试运行时，您需要指定要模拟的并发用户数量，Locust将为每个用户创建一个用户类的实例。您可以为这些类/实例添加任何您喜欢的属性，但有一些属性对Locust有特殊的意义。

### wait_time属性

用户的wait_time方法使您可以轻松地在每个任务执行后引入延迟。如果没有指定wait_time，则下一个任务将在上一个任务完成后立即执行。

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

如果文件中存在多个用户类，并且命令行上未指定用户类，则`Locust`将生成相同数量的每个用户类。您还可以通过将它们作为命令行参数传递来指定从同一`locustfile`使用哪些用户类

```shell
locust -f locust_file.py WebUser MobileUser
```

如果您希望模拟某种类型的更多用户，则可以在这些类上设置权重属性。例如，网络用户的可能性是移动用户的三倍：

```python
class WebUser(User):
    weight = 3
    ...

class MobileUser(User):
    weight = 1
    ...
```

也可以设置属性`fixed_count`。在这种情况下，权重属性将被忽略，并将生成确切的计数用户。首先生成这些用户。
在下面的示例中，只会生成一个`AdminUser`实例，以便进行一些特定的工作，独立于用户总数更准确地控制请求计数。

```python
class AdminUser(User):
    wait_time = constant(600)
    fixed_count = 1

    @task
    def restart_app(self):
        ...

class WebUser(User):
    ...
```

### on_start和on_stop方法

`Users`（以及`TaskSets`）可以定定义`on_start`方法和`on_stop`方法。当用户开始运行时，用户将调用其`on_start`方法；当用户停止运行时，用户将调用其`on_stop`方法。
对于任务集，当模拟用户开始执行该任务集时，将调用`on_start`方法，当模拟用户停止执行该任务集时（当调用`interrupt()`或用户被终止时），将调用`on_stop`方法。

## Tasks

开始负载测试时，将为每个模拟用户创建一个`User`类的实例，这些用户将开始在自己的绿色线程中运行。
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

def my_task(user):
    pass

class MyUser(User):
    tasks = [my_task]
    wait_time = constant(1)
```

将任务属性指定为列表或者字典，以下两种方式都表示执行`my_task`的概率是`another_task`的三倍

```python
tasks = [my_task, my_task, my_task, another_task]
tasks = {my_task: 3, another_task: 1}
```

### @tag装饰器

通过使用装饰器标记`@tag`任务，可以挑剔在测试期间使用`--tags`和`--exclude-tags`参数执行哪些任务。

```python
from locust import User, constant, task, tag

class MyUser(User):
    wait_time = constant(1)

    @tag('tag1')
    @task
    def task1(self):
        pass

    @tag('tag1', 'tag2')
    @task
    def task2(self):
        pass

    @tag('tag3')
    @task
    def task3(self):
        pass

    @task
    def task4(self):
        pass
```

如果使用`--tags tag1`，则在测试期间将仅执行`task1`和`task2`。如果使用`--tags tag2 tag3`它，则只会执行`task2`和`task3`。

`--exclude-tags`将以完全相反的方式行事。因此，如果使用`--exclude-tags tag3`测试，则只会执行`task1 task2 task4`。

## Events

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

## TaskSet class