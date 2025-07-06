
[Pro Git 中文版链接](https://git-scm.com/book/zh/v2)

## git使用代理
### **1. 临时设置代理（仅当前终端会话有效）**
#### **Linux/macOS**
```bash
# 设置 HTTP 代理
export http_proxy=http://proxy.example.com:8080
export https_proxy=http://proxy.example.com:8080

# 取消代理
unset http_proxy
unset https_proxy
```

#### **Windows（CMD 或 PowerShell）**
```cmd
:: 设置 HTTP 代理
set http_proxy=http://proxy.example.com:8080
set https_proxy=http://proxy.example.com:8080

:: 取消代理
set http_proxy=
set https_proxy=
```
### **2. 永久设置代理（全局配置）**
#### **通过 Git 命令配置**
```bash
# 设置 HTTP 代理
git config --global http.proxy http://proxy.example.com:8080
git config --global https.proxy http://proxy.example.com:8080

# 取消代理
git config --global --unset http.proxy
git config --global --unset https.proxy
```

#### **检查配置**
```bash
git config --global --list
```

### **3. SOCKS 代理配置**
如果使用 SOCKS 代理（如 `socks5`），需通过 `git config` 设置：
```bash
git config --global http.proxy socks5://proxy.example.com:1080
git config --global https.proxy socks5://proxy.example.com:1080
```

### **4. 忽略特定地址（不走代理）**
若需跳过某些地址（如内网），可设置 `no_proxy`：
```bash
# Linux/macOS
export no_proxy="localhost,127.0.0.1,.example.com"

# Windows
set no_proxy=localhost,127.0.0.1,.example.com
```

### **5. 代理认证（需用户名密码）**
如果代理需要认证，可在 URL 中直接指定（不推荐，密码明文暴露）：
```bash
http://username:password@proxy.example.com:8080
```

**更安全的方式**：  
使用 Git 的凭证缓存（如 `git config --global credential.helper cache`）或系统密钥管理工具。

---

### **6. 验证代理是否生效**
尝试克隆一个仓库测试：
```bash
git clone https://github.com/example/repo.git
```

如果失败，检查：
- 代理地址和端口是否正确
- 是否需要认证
- 网络防火墙是否允许代理流量

---

### **常见问题**
- **代理类型错误**：确保使用 `http`/`https` 或 `socks5` 协议。
- **权限问题**：某些系统需管理员权限设置环境变量。
- **代理服务未启动**：确认代理服务器（如 `Shadowsocks`、`V2Ray`）已运行。

---