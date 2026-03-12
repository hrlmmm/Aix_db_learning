import os
from datetime import datetime
from functools import wraps

import jwt
from sanic import response


def check_token(f):
    """
    JWT Token 校验装饰器
    
    使用方式：
    @app.get("/api/user/info")
    @check_token
    async def get_user_info(request):
        # 校验通过后，可以通过 request.ctx.user_payload 获取用户信息
        user_id = request.ctx.user_payload.get("user_id")
        return response.json({"user_id": user_id})
    """
    @wraps(f)
    async def wrapper(request, *args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return response.json({"message": "无效Token", "code": 401}, status=401)
        try:
            # 去掉 Bearer 前缀（如果有的话）
            if token.startswith("Bearer "):
                token = token.split(" ")[1]

            # 解码 JWT token
            payload = jwt.decode(token, key=os.getenv("JWT_SECRET_KEY", "550e8400-e29b-41d4-a716-446655440000"), algorithms=["HS256"])
            # 检查 token 是否过期
            if "exp" in payload and datetime.fromtimestamp(payload["exp"], tz=datetime.timezone.utc) < datetime.now(datetime.timezone.utc):
                return response.json({"message": "Token已过期", "code": 401}, status=401)

            request.ctx.user_payload = payload
        except jwt.ExpiredSignatureError as e:
            return response.json({"message": "Token已过期", "code": 401}, status=401)
        except Exception as e:
            return response.json({"message": "无效Token", "code": 401}, status=401)

        # 继续处理请求
        return await f(request, *args, **kwargs)

    return wrapper