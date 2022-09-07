# pexpect模块

[API 概述 — Pexpect 4.8 文档](https://pexpect.readthedocs.io/en/stable/overview.html)

[Python之pexpect详解 - baishuchao - 博客园 (cnblogs.com)](https://www.cnblogs.com/baishuchao/p/9339159.html)

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

