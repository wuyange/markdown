# dockerfile

## dockerfile 常用命令

```
### 1. **基础知识**

- **Dockerfile** 是用来定义镜像内容的脚本。
- 每个命令都会创建一个新的镜像层。

------

### 2. **常用命令**

#### 1. `FROM`

指定基础镜像，所有Dockerfile必须以此为起点。

​```
dockerfile


复制代码
FROM ubuntu:20.04
​```

#### 2. `RUN`

执行命令来安装软件或配置环境。

​```
dockerfile


复制代码
RUN apt-get update && apt-get install -y python3
​```

#### 3. `WORKDIR`

设置工作目录。

​```
dockerfile


复制代码
WORKDIR /app
​```

#### 4. `COPY`

复制本地文件到镜像。

​```
dockerfile


复制代码
COPY . /app
​```

#### 5. `ADD`

类似于 `COPY`，但可以解压文件或从URL下载资源。

​```
dockerfile


复制代码
ADD app.tar.gz /app
​```

#### 6. `CMD`

定义容器启动时默认执行的命令（可以被覆盖）。

​```
dockerfile


复制代码
CMD ["python3", "app.py"]
​```

#### 7. `ENTRYPOINT`

定义容器启动时执行的主命令（不易被覆盖）。

​```
dockerfile


复制代码
ENTRYPOINT ["python3", "app.py"]
​```

#### 8. `EXPOSE`

声明容器监听的端口（仅供参考，需配合运行时参数）。

​```
dockerfile


复制代码
EXPOSE 8080
​```

#### 9. `ENV`

设置环境变量。

​```
dockerfile


复制代码
ENV APP_ENV=production
​```

#### 10. `ARG`

定义构建时变量（与 `ENV` 不同，只在构建时可用）。

​```
dockerfile复制代码ARG VERSION=1.0
RUN echo "Version: $VERSION"
​```

#### 11. `LABEL`

添加元信息。

​```
dockerfile


复制代码
LABEL maintainer="your_email@example.com"
​```

#### 12. `VOLUME`

定义挂载点以支持持久化数据。

​```
dockerfile


复制代码
VOLUME /data
​```

#### 13. `USER`

指定运行容器时的用户。

​```
dockerfile


复制代码
USER nonroot
​```

------

### 3. **完整示例**

以下是一个简单的Python应用的Dockerfile示例：

​```
dockerfile复制代码# 使用Python基础镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 复制当前目录下所有内容到镜像的/app目录
COPY . /app

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 声明端口
EXPOSE 8080

# 设置环境变量
ENV APP_ENV=production

# 启动命令
CMD ["python", "app.py"]
​```

------

### 4. **构建和运行**

1. 构建镜像

   ：

   ```
   bash
   
   
   复制代码
   docker build -t my-app .
   ```

2. 运行容器

   ：

   ```
   bash
   
   
   复制代码
   docker run -p 8080:8080 my-app
   ```

------

### 5. **最佳实践**

- **多阶段构建**：用来减少镜像大小。
- **最小权限原则**：尽量使用非root用户运行容器。
- **合并命令**：减少镜像层的数量。

这些命令足够帮助你构建大多数基础镜像。需要更多细节可以随时扩展！
```





## 使用docker构建镜像的时候，有可能需要安装python以及python的三方库，但是宿主机有可能有没有网络，应该怎么保证python以及三方库可以安装成功呢

```
在宿主机没有网络的情况下，构建 Docker 镜像并安装 Python 及其第三方库的关键在于**提前准备所需文件**和**脱机安装依赖**。以下是解决方法的具体步骤：

---

### 1. **准备离线安装文件**

#### 1.1 下载 Python 安装包（如果需要）
在有网络的机器上下载目标 Python 版本的安装包：
- 如果使用 `python:base-image`，可以跳过此步骤。
- 如果自定义安装 Python，下载相关二进制文件（如 `.tar.gz` 或 `.whl`）。

#### 1.2 下载第三方库的离线包
使用 `pip download` 下载所需的库及其依赖：
​```bash
mkdir packages
pip download -r requirements.txt -d packages
​```
- `-r requirements.txt`：指定你的依赖文件。
- `-d packages`：将所有依赖包保存到本地 `packages` 目录。

将 `packages` 文件夹连同 `requirements.txt` 一起打包，准备复制到镜像中。

---

### 2. **构建支持离线安装的 Dockerfile**

编写 Dockerfile，将离线安装包复制到镜像中，并使用 `pip` 从本地文件夹安装依赖。

#### 示例：
​```dockerfile
# 使用基础镜像（带Python）
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 复制应用程序代码
COPY . /app

# 复制离线依赖包
COPY packages /packages
COPY requirements.txt /app

# 安装 Python 依赖（从离线包）
RUN pip install --no-index --find-links=/packages -r requirements.txt

# 声明端口
EXPOSE 8080

# 启动应用程序
CMD ["python", "app.py"]
​```

---

### 3. **步骤解析**
- **`--no-index`**：指示 `pip` 不从网络上搜索依赖。
- **`--find-links=/packages`**：告诉 `pip` 从 `/packages` 文件夹中查找依赖包。
- **提前准备的文件**：
  - `requirements.txt`
  - 离线包目录 `packages`

---

### 4. **构建和运行**
1. **构建镜像**
   将准备好的文件（包括 `packages` 和 `requirements.txt`）与 Dockerfile 放在同一目录中，然后运行：
   ```bash
   docker build -t my-offline-app .
   ```

2. **运行容器**
   ```bash
   docker run -p 8080:8080 my-offline-app
   ```

---

### 5. **如果需要定制 Python 安装**
1. 准备离线安装的 Python 二进制文件或源码包（如 `.tar.gz`）。
2. 在 Dockerfile 中解压并安装 Python：
   ```dockerfile
   # 解压并安装 Python
   COPY python-3.9.7.tar.gz /tmp/
   RUN tar -xzf /tmp/python-3.9.7.tar.gz -C /tmp && \
       cd /tmp/Python-3.9.7 && \
       ./configure && make && make install
   ```

---

### 6. **优点**
- **无网络依赖**：所有资源都提前准备好，确保镜像构建成功。
- **可重复性强**：即使宿主机网络不可用，镜像依然可以构建。

通过这种方式，可以有效解决宿主机没有网络的问题，同时确保 Python 和第三方库的安装顺利进行。
```

