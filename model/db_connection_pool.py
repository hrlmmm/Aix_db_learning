import logging
import os
import traceback
from contextlib import contextmanager
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase,scoped_session
from sqlalchemy.pool import QueuePool
import logging

logger = logging.getLogger(__name__)


class Base(DeclarativeBase):
    pass


class DBConnectionPool:
    """
    数据库连接池 (单例模式)
    """
    # 保证单例模式下的数据库连接池只初始化一次
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DBConnectionPool, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        try:
            if DBConnectionPool._initialized:
                return
            # 获取数据库连接URI，如果环境变量不存在则使用默认值
            database_uri = os.getenv("SQLALCHEMY_DATABASE_URI", "postgresql+psycopg2://aix_db:1@127.0.0.1:5432/aix_db")
            self.engine = create_engine(
                database_uri,
                pool_size=10,  # 连接池大小
                max_overflow=20,  # 连接池最大溢出大小
                pool_recycle=3600,  # 连接回收时间（秒），避免长时间连接失效
                pool_timeout=30,  # 连接池等待超时时间（秒）
                pool_pre_ping=True,  # 启用连接预检测，确保连接有效性
                echo=False,  # 是否打印SQL语句，用于调试
            )
            # 创建会话工厂
            self.SessionLocal = sessionmaker(bind=self.engine)
            self.Base = Base
            DBConnectionPool._initialized = True

            logger.info("Database connection pool initialized.")


        except Exception as e:
            logger.error(f"Failed to load environment variables: {e}")
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