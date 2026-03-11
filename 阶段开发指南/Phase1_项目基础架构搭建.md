# Phase 1：项目基础架构搭建

> 从零开始构建 Aix-DB 项目的第一步

---

## 📌 阶段目标

本阶段的目标是从零搭建项目骨架，配置开发环境和核心依赖。具体需要完成：

1. **创建项目目录结构** - 规范化组织代码
2. **配置 Python 虚拟环境** - 隔离项目依赖
3. **安装核心依赖** - Sanic、SQLAlchemy 等
4. **配置日志系统** - 统一的日志输出
5. **配置环境变量管理** - 集中管理配置
6. **搭建 Sanic 基础服务框架** - Web 服务入口
7. **配置数据库连接池** - 数据库访问基础

---

## 🧠 为什么要先搭建基础架构？

在企业级开发中，**基础设施先行** 是一个非常重要的原则。原因如下：

1. **统一开发环境** - 避免"在我机器上能运行"的问题
2. **规范代码组织** - 良好的目录结构是团队协作的基础
3. **日志是调试的眼睛** - 没有日志就像盲人摸象
4. **配置分离** - 环境变量是连接开发和生产的桥梁

---

## 🛠️ 详细实操步骤

### 第一步：创建项目目录结构

**目的**：将不同功能的代码放到对应的目录，便于维护和查找

在项目根目录下创建以下目录结构：

```
Aix-DB/
├── config/           # 配置模块
│   └── __init__.py
├── constants/        # 常量定义
│   └── __init__.py
├── model/           # 数据模型层
│   └── __init__.py
├── services/        # 业务逻辑层
│   └── __init__.py
├── controllers/     # API 控制器层
│   └── __init__.py
├── common/         # 公共工具模块
│   └── __init__.py
├── agent/          # 智能体模块
│   └── __init__.py
└── logs/           # 日志目录（空目录）
```

**创建命令**（在 PowerShell 中执行）：

```powershell
# 在项目根目录 d:\PycharmProjects\Aix-DB 下执行
New-Item -ItemType Directory -Path "config", "constants", "model", "services", "controllers", "common", "agent", "logs" -Force
```

**源码对照**：
- 参考完整项目的目录结构：[Aix-DB 根目录](file:///d:/PycharmProjects/Aix-DB/)

---

### 第二步：创建 Python 虚拟环境

**目的**：隔离项目依赖，避免不同项目之间的包版本冲突

**为什么要虚拟环境？**
- 假设你有两个项目 A 和 B，A 需要 Flask 1.0，B 需要 Flask 2.0
- 如果没有虚拟环境，两个项目会共用同一个 Flask，导致版本冲突
- 虚拟环境就像给每个项目分配独立的"房间"，各用各的依赖

**操作步骤**：

```powershell
# 方法一：使用 uv（推荐，速度更快）
# 先检查是否安装了 uv
uv --version

# 如果没有，先安装 uv
pip install uv

# 创建虚拟环境（Python 3.11）
uv venv --python 3.11 .venv

# 激活虚拟环境
# Windows PowerShell
.venv\Scripts\Activate.ps1

# 或者使用 uv run 直接运行（不需要激活）
uv run python your_script.py
```

```powershell
# 方法二：使用 venv（Python 内置）
# 创建虚拟环境
python -m venv .venv

# 激活虚拟环境
.venv\Scripts\Activate.ps1
```

**验证是否激活成功**：
- 命令行前会出现 `(.venv)` 前缀
- 执行 `python --version` 确认是 3.11 版本

---

### 第三步：安装核心依赖

**目的**：安装项目运行所需的基础包

**依赖说明**：

| 依赖包 | 作用 |
|--------|------|
| **sanic** | 异步 Python Web 框架，高性能 API 服务 |
| **sanic-ext** | Sanic 官方扩展，提供 OpenAPI 支持 |
| **sqlalchemy** | ORM 框架，数据库抽象 |
| **psycopg2-binary** | PostgreSQL 数据库驱动 |
| **pymysql** | MySQL 数据库驱动 |
| **python-dotenv** | 读取 .env 环境变量文件 |
| **coloredlogs** | 带颜色的日志输出 |
| **bcrypt** | 密码哈希 |
| **pyjwt** | JWT Token 生成与验证 |
| **python-multipart** | 文件上传支持 |

**安装命令**：

```powershell
# 安装核心依赖
pip install sanic sanic-ext sqlalchemy psycopg2-binary pymysql python-dotenv coloredlogs bcrypt pyjwt python-multipart

# 如果使用 uv
uv add sanic sanic-ext sqlalchemy psycopg2-binary pymysql python-dotenv coloredlogs bcrypt pyjwt python-multipart
```

**源码对照**：
- 参考完整项目的依赖列表：[requirements.txt](file:///d:/PycharmProjects/Aix-DB/requirements.txt)

---

### 第四步：配置环境变量文件

**目的**：集中管理配置，实现开发/测试/生产环境隔离

**为什么要用环境变量？**
- 数据库密码等敏感信息不应该写在代码里
- 不同环境（开发、测试、生产）需要不同的配置
- 方便部署和运维

**操作步骤**：

1. 在项目根目录创建 `.env` 文件：

```bash
# 服务配置
SERVER_HOST=0.0.0.0
SERVER_PORT=8088
SERVER_WORKERS=2

# 数据库配置（PostgreSQL）
DB_HOST=127.0.0.1
DB_PORT=5432
DB_NAME=chat_db
DB_USER=postgres
DB_PASSWORD=postgres

# MySQL 配置（可选）
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_DB=chat_db
MYSQL_USER=root
MYSQL_PASSWORD=root

# JWT 配置
JWT_SECRET=your-secret-key-change-in-production
JWT_EXPIRE_HOURS=24

# LLM 配置（可选）
OPENAI_API_KEY=sk-xxx
OPENAI_BASE_URL=https://api.openai.com/v1
```

2. 创建 `config/__init__.py` 并实现环境变量加载：

**文件**：`config/__init__.py`

```python
import os
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()

# 从环境变量读取配置
DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_NAME = os.getenv("DB_NAME", "chat_db")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")

SERVER_HOST = os.getenv("SERVER_HOST", "0.0.0.0")
SERVER_PORT = int(os.getenv("SERVER_PORT", "8088"))
SERVER_WORKERS = int(os.getenv("SERVER_WORKERS", "2"))

JWT_SECRET = os.getenv("JWT_SECRET", "default-secret-key")
JWT_EXPIRE_HOURS = int(os.getenv("JWT_EXPIRE_HOURS", "24"))
```

**源码对照**：
- 完整实现：[config/load_env.py](file:///d:/PycharmProjects/Aix-DB/config/load_env.py)

---

### 第五步：配置日志系统

**目的**：统一的日志输出，便于调试和问题排查

**为什么要日志？**
- 记录程序运行状态
- 排查错误和问题
- 监控程序行为

**操作步骤**：

1. 创建日志配置文件 `config/logging.conf`：

```ini
[loggers]
keys=root,aixtdb

[handlers]
keys=consoleHandler,fileHandler

[formatters]
keys=coloredFormatter,fileFormatter

[logger_root]
level=INFO
handlers=consoleHandler,fileHandler

[logger_aixtdb]
level=INFO
handlers=consoleHandler,fileHandler
qualname=aixtdb
propagate=0

[handler_consoleHandler]
class=StreamHandler
level=INFO
formatter=coloredFormatter
args=(sys.stdout,)

[handler_fileHandler]
class=FileHandler
level=INFO
formatter=fileFormatter
args=('logs/assistant.log', 'a', 'utf-8')

[formatter_coloredFormatter]
format=%(levelname)-8s | %(asctime)s | %(name)s | %(message)s
datefmt=%Y-%m-%d %H:%M:%S

[formatter_fileFormatter]
format=%(levelname)-8s | %(asctime)s | [PID:%(process)d] | %(filename)s:%(lineno)d | %(funcName)s() | %(message)s
datefmt=%Y-%m-%d %H:%M:%S
```

2. 在 `config/load_env.py` 中添加日志配置加载逻辑：

```python
import logging
import logging.config

def setup_logging():
    """配置日志系统"""
    # 确保日志目录存在
    os.makedirs("logs", exist_ok=True)
    
    # 加载日志配置
    config_path = "config/logging.conf"
    if os.path.exists(config_path):
        logging.config.fileConfig(config_path, disable_existing_loggers=False)
    else:
        # 备用配置
        logging.basicConfig(
            level=logging.INFO,
            format="%(levelname)-8s | %(asctime)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
```

**源码对照**：
- 完整实现：[config/load_env.py](file:///d:/PycharmProjects/Aix-DB/config/load_env.py)（第 1-80 行）
- 日志配置：[config/logging.conf](file:///d:/PycharmProjects/Aix-DB/config/logging.conf)

---

### 第六步：搭建 Sanic 基础服务框架

**目的**：创建 Web 服务入口，实现 API 服务的启动

**Sanic 是什么？**
- Sanic 是一个基于 Python 的异步 Web 框架
- 类似于 Flask，但是是异步的，性能更高
- 非常适合需要处理大量并发请求的场景

**操作步骤**：

1. 创建服务入口文件 `serv.py`：

```python
import os

# 避免 OpenMP 冲突（重要！）
os.environ.setdefault("KMP_DUPLICATE_LIB_OK", "TRUE")

from sanic import Sanic
from sanic.response import empty

# 导入配置（会自动加载环境变量和日志）
from config.load_env import load_env
load_env()

# 导入日志配置
import logging
root_logger = logging.getLogger()
if not root_logger.handlers:
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)-8s | %(asctime)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        force=True,
    )

# 创建 Sanic 应用
app = Sanic("Aix-DB", configure_logging=False)

# 健康检查接口
@app.get("/health")
async def health_check(request):
    return {"status": "ok"}

# 根路径
@app.get("/")
async def root(request):
    return {"message": "Aix-DB API is running"}

# 启动服务
if __name__ == "__main__":
    import logging
    logger = logging.getLogger(__name__)
    
    host = os.getenv("SERVER_HOST", "0.0.0.0")
    port = int(os.getenv("SERVER_PORT", "8088"))
    workers = int(os.getenv("SERVER_WORKERS", "2"))
    
    logger.info(f"Starting Aix-DB server on {host}:{port}")
    
    app.run(
        host=host,
        port=port,
        workers=workers,
        access_log=True
    )
```

**源码对照**：
- 完整实现：[serv.py](file:///d:/PycharmProjects/Aix-DB/serv.py)

---

### 第七步：配置数据库连接池

**目的**：统一管理数据库连接，提高性能

**为什么要连接池？**
- 每次请求都创建新连接会很慢
- 连接池预先建立一组连接，用的时候取一个，用完归还
- 避免数据库连接数过多

**操作步骤**：

1. 创建 `model/__init__.py`：

```python
# 模型层入口
from model.db_models import *
from model.schemas import *
```

2. 创建 `model/db_connection_pool.py`：

```python
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.pool import QueuePool

class DBConnectionPool:
    """数据库连接池"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        # PostgreSQL 连接字符串
        db_host = os.getenv("DB_HOST", "127.0.0.1")
        db_port = os.getenv("DB_PORT", "5432")
        db_name = os.getenv("DB_NAME", "chat_db")
        db_user = os.getenv("DB_USER", "postgres")
        db_password = os.getenv("DB_PASSWORD", "postgres")
        
        self.database_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        
        # 创建引擎（带连接池）
        self.engine = create_engine(
            self.database_url,
            poolclass=QueuePool,
            pool_size=10,          # 最小连接数
            max_overflow=20,       # 最大额外连接数
            pool_pre_ping=True,    # 使用前测试连接
            echo=False             # 是否打印 SQL 语句
        )
        
        # 创建会话工厂
        self.session_factory = sessionmaker(bind=self.engine)
        self.ScopedSession = scoped_session(self.session_factory)
        
        self._initialized = True
    
    def get_session(self):
        """获取数据库会话"""
        return self.ScopedSession()
    
    def close(self):
        """关闭所有连接"""
        self.ScopedSession.remove()

# 全局单例
_pool = DBConnectionPool()

def get_db_pool():
    """获取数据库连接池实例"""
    return _pool
```

**源码对照**：
- 完整实现：[model/db_connection_pool.py](file:///d:/PycharmProjects/Aix-DB/model/db_connection_pool.py)

---

## ✅ 阶段验收标准

完成本阶段后，你应该能够：

1. ✅ 项目目录结构清晰，符合规范
2. ✅ Python 虚拟环境正常激活
3. ✅ 核心依赖已安装
4. ✅ `.env` 文件配置正确
5. ✅ 日志系统正常工作
6. ✅ Sanic 服务能够启动：`python serv.py`
7. ✅ 访问 `http://localhost:8088/health` 返回 `{"status": "ok"}`

---

## 🧪 测试验证

**测试 1：启动服务**

```powershell
# 在虚拟环境中运行
python serv.py
```

如果看到类似以下输出，说明启动成功：
```
INFO | 2026-03-10 12:00:00 | Starting Aix-DB server on 0.0.0.0:8088
```

**测试 2：健康检查**

打开浏览器访问：`http://localhost:8088/health`

应该返回：
```json
{"status": "ok"}
```

**测试 3：日志输出**

检查 `logs/assistant.log` 文件是否有日志内容。

---

## 📚 源码对照汇总表

| 功能模块 | 参考文件 | 行号 |
|----------|----------|------|
| 服务入口 | [serv.py](file:///d:/PycharmProjects/Aix-DB/serv.py) | 1-100 |
| 环境变量加载 | [config/load_env.py](file:///d:/PycharmProjects/Aix-DB/config/load_env.py) | 1-80 |
| 日志配置 | [config/logging.conf](file:///d:/PycharmProjects/Aix-DB/config/logging.conf) | - |
| 数据库连接池 | [model/db_connection_pool.py](file:///d:/PycharmProjects/Aix-DB/model/db_connection_pool.py) | - |

---

## ⚠️ 常见问题

### Q1: 启动报错 "ModuleNotFoundError: No module named 'sanic'"
**解决**：确保虚拟环境已激活，然后重新安装依赖

### Q2: 报错 "database 'chat_db' does not exist"
**解决**：需要先在 PostgreSQL 中创建数据库

```sql
CREATE DATABASE chat_db;
```

### Q3: 日志文件没有生成
**解决**：检查 `logs` 目录是否有写权限，确保目录已创建

---

## 🚀 下一步

完成 Phase 1 后，你将进入 **Phase 2：数据库模型与数据层建设**。

在下一阶段，我们将：
- 设计并创建核心数据表
- 实现 SQLAlchemy ORM 模型类
- 实现数据库初始化脚本

---

**✅ Phase 1 开发指南完成！**
