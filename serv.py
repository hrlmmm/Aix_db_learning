import os

# 避免本地向量/Embedding 库重复初始化 OpenMP 导致崩溃或卡死
# 参考错误: "OMP: Error #15: Initializing libomp.dylib, but found libomp.dylib already initialized."
os.environ.setdefault("KMP_DUPLICATE_LIB_OK", "TRUE")

from sanic import Sanic
from sanic.response import empty, json
from sanic.worker.manager import WorkerManager
from controllers.user_rest_api import bp as user_bp

# 设置 worker 启动超时时间（单位：0.1秒）
# 设置为 180 秒（1800 * 0.1秒），允许 workers 有足够时间完成启动
startup_timeout_seconds = int(os.getenv("SANIC_WORKER_STARTUP_TIMEOUT", 180))
WorkerManager.THRESHOLD = startup_timeout_seconds * 10  # 转换为 0.1 秒单位

import controllers
# from common.route_utility import autodiscover
from config.load_env import load_env

load_env()

import logging
root_logger = logging.getLogger()
if not root_logger.handlers:
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)-8s | %(asctime)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        force=True,
    )

# 创建 Sanic 应用实例
app = Sanic("Aix-DB", configure_logging=False)
app.blueprint(user_bp)
@app.get("/health")
async def health_check(request):
    return json({"status": "OK"})

@app.get("/")
async def root(request):
    return json({"message": "Hello, Aix-DB!"})

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