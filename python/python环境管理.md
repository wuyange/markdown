# Python环境管理

## 使用pyenv管理不同的python版本

在 Python 开发中，使用 `uv` 工具可以高效管理 Python 版本和依赖包。以下是详细的使用指南，涵盖安装、版本管理、虚拟环境创建和依赖包管理等核心功能。

---

### **安装 uv**
#### 1. **通过官方脚本安装（推荐）**
- **Linux/macOS**：
  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```
- **Windows**（以管理员权限运行 PowerShell）：
  ```powershell
  powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
  ```

#### 2. **通过 pip 安装**
```bash
pip install uv
```

#### 3. **验证安装**
```bash
uv --version
```
输出示例：`uv 0.1.0`

---

### **管理 Python 版本**
#### 1. **安装指定版本的 Python**
```bash
# 安装最新稳定版 Python
uv python install

# 安装特定版本（如 Python 3.12）
uv python install 3.12

# 安装多个版本
uv python install 3.11 3.12

# 安装 PyPy 实现
uv python install pypy@3.10
```

#### 2. **查看已安装的 Python 版本**
```bash
uv python list
```
输出示例：
```
3.9.18 (CPython)
3.11.5 (CPython)
3.12.0 (CPython)
3.10.12 (PyPy)
```

#### 3. **切换 Python 版本**
```bash
# 切换到 Python 3.12
uv python use 3.12

# 切换到 PyPy 3.10
uv python use pypy@3.10
```

#### 4. **重新安装 Python 版本**
```bash
# 重新安装 Python 3.12（修复已知问题）
uv python install --reinstall 3.12
```

---

### **创建虚拟环境**
#### 1. **创建虚拟环境并指定 Python 版本**
```bash
# 创建虚拟环境（使用默认 Python 版本）
uv venv

# 指定 Python 版本创建虚拟环境
uv venv --python 3.12

# 指定 PyPy 版本创建虚拟环境
uv venv --python pypy@3.10
```

#### 2. **激活虚拟环境**
- **Linux/macOS**：
  ```bash
  source .venv/bin/activate
  ```
- **Windows**：
  ```bash
  .\.venv\Scripts\activate
  ```

#### 3. **退出虚拟环境**
```bash
deactivate
```

---

### **管理依赖包**
#### 1. **安装依赖包**
```bash
# 安装单个包
uv pip install numpy

# 安装多个包
uv pip install numpy pandas

# 从 requirements.txt 安装
uv pip install -r requirements.txt
```

#### 2. **生成依赖文件**
```bash
# 生成 requirements.txt
uv pip freeze > requirements.txt
```

#### 3. **生成依赖锁文件**
```bash
# 从 pyproject.toml 生成锁定文件
uv pip compile pyproject.toml -o requirements.txt

# 从 requirements.in 生成锁定文件
uv pip compile requirements.in
```

#### 4. **同步依赖**
```bash
# 根据 requirements.txt 精确安装依赖
uv pip sync requirements.txt
```

#### 5. **升级包**
```bash
# 升级所有包
uv pip install --upgrade-all

# 升级指定包
uv pip install --upgrade numpy
```

---

### **常见问题与优化**
#### 1. **更换镜像源**
- **临时使用镜像源**：
  ```bash
  uv pip install -i https://pypi.tuna.tsinghua.edu.cn/simple numpy
  ```
- **永久配置镜像源**：
  ```bash
  # 添加环境变量（推荐加入 shell 配置文件）
  export UV_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple
  ```

#### 2. **清理缓存**
```bash
uv clean
```

#### 3. **处理 SSL 错误**
```bash
# 更新证书
uv pip install --upgrade certifi
```

#### 4. **指定架构安装**
```bash
# 安装 macOS ARM64 架构的包
UV_CROSS_PLATFORM=macos-arm64 uv pip install numpy
```

---

### **六、性能优势**
- **安装速度**：`uv` 的依赖解析和安装速度比 `pip` 快 **10-100 倍**。
- **示例对比**：
  | 操作               | `pip` 用时 | `uv` 用时 | 提升 |
  |--------------------|------------|-----------|------|
  | 安装 `numpy`       | 12.3s      | 0.9s      | 13x  |
  | 创建虚拟环境       | 2.1s       | 0.3s      | 7x   |
  | 批量安装 30 个包   | 86s        | 4.2s      | 20x  |

---

### **项目初始化与依赖管理**
#### 1. **初始化项目**
```bash
# 初始化项目（自动创建 pyproject.toml）
uv init myproject

# 初始化项目并指定 Python 版本
uv init myproject -p 3.12
```

#### 2. **添加/移除依赖**
```bash
# 添加依赖（更新 pyproject.toml）
uv add flask

# 移除依赖
uv remove flask

# 向脚本添加隔离依赖
uv add --script example.py requests
```

#### 3. **同步项目依赖**
```bash
# 同步依赖（根据 pyproject.toml）
uv sync

# 升级依赖
uv sync --upgrade
```

---

### 使用uv install 安装 python慢

通过手动下载 Python 安装包并设置本地镜像目录，可以显著提升安装速度。

#### **步骤 1：手动下载 Python 安装包**
1. **访问官方发布页面**：
   - [https://github.com/astral-sh/python-build-standalone/releases](https://github.com/astral-sh/python-build-standalone/releases)
2. **选择需要的版本**（例如 `20250409`）：
   - 根据操作系统和架构（如 `x86_64-linux` 或 `x86_64-pc-windows-msvc`）下载对应的 `.tar.gz` 文件。
   - 示例文件名：
     ```
     cpython-3.10.17+20250409-x86_64-unknown-linux-gnu-install_only_stripped.tar.gz
     cpython-3.11.12+20250409-x86_64-unknown-linux-gnu-install_only_stripped.tar.gz
     ```

3. **创建本地镜像目录**：
   ```bash
   # Linux/macOS
   mkdir -p ~/uv_python_mirror/20250409
   # Windows
   mkdir C:\uv_python_mirror\20250409
   ```

4. **将下载的 `.tar.gz` 文件移动到镜像目录**：
   ```bash
   # Linux/macOS
   mv cpython-3.10.17+20250409-*.tar.gz ~/uv_python_mirror/20250409/
   # Windows（使用资源管理器或命令行）
   move cpython-3.10.17+20250409-*.tar.gz C:\uv_python_mirror\20250409\
   ```

#### **步骤 2：设置环境变量**
1. **Linux/macOS**：
   ```bash
   export UV_PYTHON_INSTALL_MIRROR=file://~/uv_python_mirror/20250409
   ```
2. **Windows**：
   - 打开终端（PowerShell 或 CMD），执行：
     ```cmd
     setx UV_PYTHON_INSTALL_MIRROR "file:///C:/uv_python_mirror/20250409"
     ```
   - 或临时设置（仅当前会话生效）：
     ```cmd
     set UV_PYTHON_INSTALL_MIRROR=file:///C:/uv_python_mirror/20250409
     ```

#### **步骤 3：验证镜像配置**
```bash
uv python install 3.10
```
此时 `uv` 会直接从本地镜像目录读取文件，安装速度显著提升。



## 使用内置的venv模块创建虚拟环境

1. 创建虚拟环境test

```shell
python3 -m venv test
```

2. 激活虚拟环境test

```shell
source test/bin/activate
```

3. 退出虚拟环境

```shell
deactivate
```

### 使用requirements.txt

1. 生成依赖文件

```Bash
pip freeze > requirements.txt
```

2. 安装依赖

```Bash
pip install -r requirements.txt
```



## 使用 Anaconda 管理 Python 版本和环境

1. 创建 Python 环境 打开 Anaconda Prompt（Windows）或 Terminal（Mac/Linux），使用 conda create 命令创建 Python 环境，例如：

```
conda create -n myenv python=3.8
```

这条命令会创建一个名为 myenv 的 Python 3.8 环境。可以根据需要安装其他需要的包，例如：

```
conda install numpy pandas matplotlib
```

2. 激活 Python 环境 创建完环境后，使用 conda activate 命令激活环境，例如：

```
conda activate myenv
```

激活后，所有的 Python 包和命令都会从该环境中获取。

3. 退出 Python 环境 在环境中完成工作后，可以使用 conda deactivate 命令退出环境，例如：

```
conda deactivate
```

4. 列出环境 可以使用 conda env list 命令列出所有的 Python 环境：

```
conda env list
```

这条命令会列出当前系统中所有的 Python 环境。

5. 删除环境 可以使用 conda remove 命令删除指定的 Python 环境，例如：

```
conda remove -n myenv --all
```

   这条命令会删除名为 myenv 的 Python 环境和其中的所有包。

6. 查看当前环境下已安装的包

```
conda list
# 查看某个指定环境的已安装包
conda list -n venv
```

7. 更新/删除某个包

```
# 更新package
conda update -n myenv numpy

# 删除package
conda remove -n myenv numpy
```

## 设置PIP源

```bash
tee /etc/pip.conf << 'EOF'
[global]
index-url = https://pypi.tuna.tsinghua.edu.cn/simple
trusted-host = pypi.tuna.tsinghua.edu.cn
EOF
```