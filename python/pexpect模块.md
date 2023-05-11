# pexpect模块

[API 概述 — Pexpect 4.8 文档](https://pexpect.readthedocs.io/en/stable/overview.html)

[Python之pexpect详解 - baishuchao - 博客园 (cnblogs.com)](https://www.cnblogs.com/baishuchao/p/9339159.html)

## 安装和简介

- 只能在linux上使用
- Pexpect是一个Python模块，用于生成子应用程序并自动控制它们。Pexpect可用于自动化交互式应用程序，如ssh，ftp，passwd，telnet等。它可用于自动化安装脚本，以在不同服务器上复制软件包安装。
- 它可用于自动化软件测试

```shell
pip install pexpect -i http://pypi.douban.com/simple --trusted-host pypi.douban.com
```

## 使用

`Pexpect`系统有两个主要接口;它们是函数`run()`和类`spawn`。`spawn`类更强大。`run()`函数比`spawn`更简单，有利于快速调用程序。当您调用`run()`函数时，它会执行给定的程序，然后返回输出,是`os.system()`的一个方便替换。

### spawn

```python
class pexpect.spawn(command, args=[], timeout=30, maxread=2000, searchwindowsize=None, logfile=None, cwd=None, env=None, ignore_sighup=False, echo=True, preexec_fn=None, encoding=None, codec_errors='strict', dimensions=None, use_poll=False)
```

部分参数说明：

- `command`: 启动一个新的子进程的命令

  ```python
  # pexpect不解释shell元字符，如重定向、管道或通配符(>、|或*)。
  # 如果想运行一个命令并将其通过另一个命令传递，那么还必须启动一个shell。例如:
child = pexpect.spawn('/bin/bash -c "ls -l | grep LOG > logs.txt"')
  ```

- `timeout`: 超时时间，指定`spawn`对象的默认超时时间。如果在`timeout`秒内没有收到期望的输出，则抛出一个`pexpect.exceptions.TIMEOUT`异常

- `maxread`: 设置读缓冲区的大小。这是`pexpect`一次尝试从`TTY`读取的最大字节数。将`maxread`大小设置为1将关闭缓冲,将`maxread`值设置得更高可能有助于从子进程中读回大量输出的情况下的性能。这个特性与`searchwindowsize`结合起来很有用。

- `searchwindowsize`: 设置搜索的的字节数，如果为默认值`None`时，将在每次迭代接收传入数据时搜索完整缓冲区，`searchwindowsize`参数是与`maxread`参数一起合作使用的，可以显著减少缓存中有很多字符时的匹配时间。

- `logfile`: 日志文件名，指定日志文件的名称和路径。如果指定了此参数，则`spawn`对象的输出将被写入到日志文件中。也可以设置日志文件名为`sys.stdout`，将日志打印到控制台

  ```python
  # 方式1
  child = pexpect.spawn('some_command',logfile = sys.stdout)
  # 方式2
  child = pexpect.spawn('some_command')
  child.logfile = open("log.log","w")
  
  # child.logfile 会记录从屏幕读取的内容，又记录输入的命令
  # 但是这样会将输入的内容记录两边
  
  # 只记录从输入的内容
  child.logfile_send = sys.stdout
  # 只记录从屏幕读取的内容，建议使用此方式
  child.logfile_read = sys.stdout
  ```

- `encoding`: 字符编码，指定`spawn`对象的字符编码。默认为 `utf-8`。

- `cwd`: 子进程的工作目录，指定子进程的当前工作目录

- `env`：子进程的环境变量，指定子进程的环境变量。

  ```python
  # 将本机的环境变量复制，并传入子进程
  env = os.environ.copy()
  proccess = pexpect.spawn('/bin/bash', env=env)
  
  # 设置环境变量name为xxxx
  proccess = pexpect.spawn('/bin/bash', env={'name':'xxxx'})
  proccess.expect_exact(']#')
  proccess.sendline('echo $name')
  
  # 环境变量无法带入ssh中
  proccess = pexpect.spawn('ssh root@10.182.79.36', env={'name':'xxxx'})
  proccess.sendline('echo $name')
  ```

- `ignore_sighup`：是否忽略 SIGHUP 信号，如果设置为`True`，则`spawn`对象在收到 SIGHUP 信号时不会退出。

- `echo`：是否回显输出，如果设置为`True`，则`spawn`对象的输出将同时输出到屏幕和日志文件中。

- `encoding`：字符编码，指定`spawn`对象的字符编码。默认为`utf-8`。

- `codec_errors`：字符编码错误处理方式，默认值是`strict`，表示编码/解码错误会引发UnicodeError异常;如果想要忽略这些错误，可以将`codec_errors`设置为`ignore`，这样就会在出现编码/解码错误时跳过错误的字符而不是抛出异常

- `use_poll`：是否使用轮询模式，默认为`True`。如果设置为`False`，则使用`select`模式。

>pexpect不解释shell元字符，如重定向、管道或通配符(>、|或*)。如果想运行一个命令并将其通过另一个命令传递，那么还必须启动一个shell。例如:
>
>```python
>child = pexpect.spawn('/bin/bash -c "ls -l | grep LOG > logs.txt"')
>```

#### expect

```python
expect(pattern, timeout=-1, searchwindowsize=-1, async_=False, **kw)
```





### run

```python
pexpect.run(command, timeout=30, withexitstatus=False, events=None, extra_args=None, logfile=None, cwd=None, env=None, **kwargs)
```

这个函数运行给定的命令;等待它完成;然后以字符串形式返回所有输出。STDERR包含在输出中。如果没有给出该命令的完整路径，则搜索该路径。

注意，即使在类unix系统上，代码行也以CR/LF (rn)组合终止，因为这是pseudottys的标准。如果你设置“withexitstatus”为true，那么run将返回一个(command_output, exitstatus)元组。如果' withexitstatus '为false，则只返回command_output。

run()函数通常可以用来代替创建一个衍生实例



```python
import pexpect
pexpect.run('ls -la')
```





```python
#只能在linux上使用
#Pexpect是一个Python模块，用于生成子应用程序并自动控制它们。Pexpect可用于自动化交互式应用程序，
#如ssh，ftp，passwd，telnet等。它可用于自动化安装脚本，以在不同服务器上复制软件包安装。
#它可用于自动化软件测试。

pexpect.run(command,event=None) # 类似os.system() 执行指定的程序，然后返回输出
>>>pexpect.run('ssh yushun@10.182.79.36', events={'\?':"yes",'word:':'hillstone'},logfile = sys.stdout,encoding='utf-8')
yushun@10.182.79.36's password: hillstone

#执行一个程序，它返回这个程序的操作句柄，以后可以通过操作这个句柄来对这个程序进行操作
pexpect.spawn(command, args=[],timeout=30,maxread=2000,searchwindowsize=None,logfile=None,enconding=None) 

child = pexpect.spawn('ssh user@10.182.79.36')
child = pexpect.spawn('ls -l /root')
child = pexpect.spawn('ssh', ['user@example.com'])
child = pexpect.spawn('ls', ['-l', '/root'])
#pexpect 不会解释 shell 元字符，如重定向(>、<)、管道(|)或通配符(*、.)
child = pexpect.spawn("ls -l | grep LOG > logs.txt")   #错误示范
child = pexpect.spawn('/bin/bash -c "ls -l | grep LOG > logs.txt"')
child = pexpect.spawn('/bin/bash', ['-c', 'ls -l | grep LOG > logs.txt'])

maxread 设置读取缓冲区大小,pexpect一次尝试读取的最大字节数,将最大读取大小设置为1将关闭缓冲
searchwindowsize 设置搜索的的字节数，如果为默认值None时，将在每次迭代接收传入数据时搜索完整缓冲区

timeout 设置超时时间，默认等待30秒，当设置为None时，则永远都不会超时

logfile 设置日志出入到文件或者控制台，即记录从屏幕读取的内容，又记录输入的命令
#两种使用方法
child = pexpect.spawn('some_command',logfile = sys.stdout)
child.logfile = open("log.log","w")

logflie.read = sys.stdout  只记录从屏幕读取的内容
logflie.send = sys.stdout  只记录输入的命令

#流中进行搜索，直到匹配到期望的模式为止
child.expect(pattern, timeout=-1)
pattern 指定要匹配的模式，可以是字符串、正则表达式、pexpect.EOF、pexpect.TIMEOUT，或者这些类型组成的列表
pexpect.EOF  匹配终止信号,检查 ssh/ftp/telnet 连接是否终止，文件是否已经到达末尾等
pexpect.TIMEOUT  用来匹配超时的情况
>>>child = pexpect.spawn('python3.9')
>>>child.sendline('exit()')
7
>>>child.expect(pexpect.EOF)
0

index = child.expect(['good', 'bad', pexpect.EOF, pexpect.TIMEOUT])
if index == 0:
    do_something()
elif index == 1:
    do_something_else()
elif index == 2:
    do_some_other_thing()
elif index == 3:
    do_something_completely_different()
    
child.expect_exact(pattern,timeout=-1)  #和expect()类似，但是是精确匹配字符串

child.send(command)   #发送命令到子程序,并返回输入多少字符
child.sendline(command)  #发送命令到子程序，且自带换行，并返回输入多少字符
child.write(command)  #和send类似，不过没有返回值
>>>child.send("python3.9")
9
>>>child.sendline("python3.9")
10
>>>child.write("python3.9")

child.sendcontrol(command) #发送CTRL-C或CTRL-Z等
child.sendcontrol("z")
       
```

