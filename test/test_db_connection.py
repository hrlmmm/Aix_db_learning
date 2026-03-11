#!/usr/bin/env python3
"""
数据库连接池测试脚本
用于检验数据库连接池是否正常工作
"""

import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from sqlalchemy import text
from model.db_connection_pool import get_db_pool

def test_db_connection():
    """测试数据库连接池"""
    print("=== 测试数据库连接池 ===")
    
    try:
        # 获取数据库连接池
        db_pool = get_db_pool()
        print("✓ 数据库连接池实例获取成功")
        
        # 获取数据库引擎
        engine = db_pool.get_engine()
        print("✓ 数据库引擎获取成功")
        
        # 测试连接
        with engine.connect() as connection:
            # 执行简单的查询
            result = connection.execute(text("SELECT 1"))
            value = result.scalar()
            print(f"✓ 数据库连接测试成功，返回值: {value}")
        
        # 测试会话
        session = db_pool.get_session()
        print("✓ 数据库会话获取成功")
        session.close()
        print("✓ 数据库会话关闭成功")
        
        print("\n🎉 所有测试通过！数据库连接池工作正常")
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_db_connection()
