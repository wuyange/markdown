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
>2gevent是一个基于libev或libuv的Python网络库，它实现了绿色线程的概念。通过使用gevent，您可以在单个线程中运行多个绿色gevent线程，这些线程可以在遇到网络IO或其他阻塞操作时自动切换，从而充分利用CPU资源，并提高并发性能。

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