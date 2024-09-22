# fiddler

Fiddler 是一个功能强大的网络调试代理工具，主要用于捕获和分析 HTTP 和 HTTPS 流量。以下是 Fiddler 的一些用途和功能：

### 用途

1. **捕获网络流量**

   - 拦截并查看所有经过的 HTTP/HTTPS 请求和响应。
   - 支持各种浏览器和应用程序。

2. **调试和分析**
- 检查请求和响应的详细信息，包括头部、Cookie、内容等。
   - 分析性能瓶颈，查看请求的时间线。
   
3. **修改请求和响应**
- 可以手动或自动修改请求和响应，用于测试不同的场景，通过rules->automatic breakpoints- >before/after request
   - 支持脚本编写，通过 FiddlerScript 自定义流量处理。
   - 支持模拟响应，通过autoresponder

4. **安全测试**

   - 测试应用程序的安全性，模拟中间人攻击。
   - 解密 HTTPS 流量以查看加密内容。

5. **流量重放**

   - 重放捕获的请求，测试服务器的响应行为。
6. **模拟弱网环境**，通过rules->performance->simulate- modem speeds

### 其他功能

- **过滤器**: 只显示特定类型的流量。
- **自动化**: 使用脚本进行自动化测试和操作。
- **插件支持**: 扩展功能以满足特定需求。

[Fiddler抓包工具保姆级使用教程（超详细）_抓包软件怎么使用-CSDN博客](https://blog.csdn.net/Mubei1314/article/details/122389950)

[Fiddler抓包配置和使用（全网最详细教程）_fiddler 配置在线-CSDN博客](https://blog.csdn.net/qq_22803691/article/details/104243501)

[fiddler之模拟响应、修改请求或响应数据（断点） - 飘着的石头 - 博客园 (cnblogs.com)](https://www.cnblogs.com/smallstone2018/p/9858004.html)



[全网最详细，Fiddler抓包实战 - 手机APP端https请求（超详细）_fiddler抓包手机app-CSDN博客](https://blog.csdn.net/qq_56271699/article/details/131603705)