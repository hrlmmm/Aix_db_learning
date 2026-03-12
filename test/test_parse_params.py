import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from sanic import Sanic, Request
from sanic_testing import TestManager
from common.param_parser import parse_params
from pydantic import BaseModel

class UserModel(BaseModel):
    name: str
    age: int

app = Sanic("Test")

@app.post("/test")
@parse_params
async def handler(request: Request, user: UserModel):
    return {"name": user.name, "age": user.age}

# 创建测试管理器
test_manager = TestManager(app)

# 测试有效参数
def test_valid_params():
    request, response = test_manager.test_client.post(
        "/test",
        json={"name": "Alice", "age": 25}
    )
    
    assert response.status == 200
    assert response.json == {"name": "Alice", "age": 25}
    print("✓ 有效参数测试通过")

# 测试缺少必需参数
def test_missing_age():
    request, response = test_manager.test_client.post(
        "/test",
        json={"name": "Bob"}
    )
    
    assert response.status == 400
    print("✓ 缺少必需参数测试通过")

# 测试参数类型错误
def test_invalid_age_type():
    request, response = test_manager.test_client.post(
        "/test",
        json={"name": "Charlie", "age": "thirty"}
    )
    
    assert response.status == 400
    print("✓ 参数类型错误测试通过")

# 测试空请求体
def test_empty_body():
    request, response = test_manager.test_client.post(
        "/test",
        json={}
    )
    
    assert response.status == 400
    print("✓ 空请求体测试通过")

# 测试额外字段
def test_extra_fields():
    request, response = test_manager.test_client.post(
        "/test",
        json={"name": "David", "age": 30, "extra": "field"}
    )
    
    assert response.status == 200
    assert response.json == {"name": "David", "age": 30}
    print("✓ 额外字段测试通过")

# 运行所有测试
def run_all_tests():
    print("开始测试 parse_params 装饰器...\n")
    
    try:
        test_valid_params()
        test_missing_age()
        test_invalid_age_type()
        test_empty_body()
        test_extra_fields()
        print("\n所有测试完成！")
    except AssertionError as e:
        print(f"\n✗ 测试失败: {e}")
        raise
    except Exception as e:
        print(f"\n✗ 测试出错: {e}")
        raise

if __name__ == "__main__":
    run_all_tests()
