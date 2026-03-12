import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
from common.exception import MyException
from constants.code_enum import SysCodeEnum

# 抛出自定义异常
raise MyException(SysCodeEnum.DATA_NOT_FOUND, "用户不存在")
