import datetime
from typing import Optional

from sqlalchemy import (
    BigInteger,
    Boolean,
    Integer,
    String,
    TIMESTAMP,
    Text,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column

from model.db_connection_pool import Base

class TUser(Base):
    """用户表"""
    __tablename__ = "t_user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_name: Mapped[Optional[str]] = mapped_column(String(200), comment="用户名称")
    password: Mapped[Optional[str]] = mapped_column(String(300), comment="密码")
    mobile: Mapped[Optional[str]] = mapped_column(String(100), comment="手机号")
    role: Mapped[Optional[str]] = mapped_column(String(20), default="user", comment="角色: admin/user")
    create_time: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP, comment="创建时间")
    update_time: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP, comment="修改时间")

class TUserQaRecord(Base):
    """用户问答记录表"""
    __tablename__ = "t_user_qa_record"
    __table_args__ = {"comment": "用户问答记录表"}

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    user_id: Mapped[Optional[int]] = mapped_column(Integer, comment="用户ID")
    uuid: Mapped[Optional[str]] = mapped_column(String(200), comment="uuid")
    conversation_id: Mapped[Optional[str]] = mapped_column(String(100), comment="对话ID")
    message_id: Mapped[Optional[str]] = mapped_column(String(100), comment="消息ID")
    task_id: Mapped[Optional[str]] = mapped_column(String(100), comment="任务ID")
    chat_id: Mapped[Optional[str]] = mapped_column(String(100), comment="聊天ID")
    question: Mapped[Optional[str]] = mapped_column(Text, comment="问题")
    to2_answer: Mapped[Optional[str]] = mapped_column(Text, comment="LLM回答")
    to4_answer: Mapped[Optional[str]] = mapped_column(Text, comment="业务数据")
    qa_type: Mapped[Optional[str]] = mapped_column(String(100), comment="问答类型")
    datasource_id: Mapped[Optional[int]] = mapped_column(BigInteger, comment="数据源ID")
    file_key: Mapped[Optional[str]] = mapped_column(String(100), comment="文件minio/key")
    sql_statement: Mapped[Optional[str]] = mapped_column(Text, comment="SQL语句(数据问答时保存)")
    create_time: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), comment="创建时间")

class TAiModel(Base):
    """AI模型表"""
    __tablename__ = "t_ai_model"
    __table_args__ = {"comment": "AI模型表"}
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    supplier: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        comment="供应商: 1:OpenAI, 2:Azure, 3:Ollama, 4:vLLM, 5:DeepSeek, 6:Qwen, 7:Moonshot, 8:ZhipuAI, 9:Other",
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False, comment="模型名称")
    model_type: Mapped[int] = mapped_column(Integer, nullable=False, comment="模型类型: 1:LLM, 2:Embedding, 3:Rerank")
    base_model: Mapped[str] = mapped_column(String(255), nullable=False, comment="基础模型")
    default_model: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False, comment="是否默认")
    api_key: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, comment="API Key")
    api_domain: Mapped[str] = mapped_column(String(255), nullable=False, comment="API Domain")
    protocol: Mapped[int] = mapped_column(Integer, default=1, nullable=False, comment="协议: 1:OpenAI, 2:Ollama")
    config: Mapped[Optional[str]] = mapped_column(Text, comment="配置JSON")
    status: Mapped[int] = mapped_column(Integer, default=1, nullable=False, comment="状态: 1:正常")
    create_time: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP, comment="创建时间")

class TDsRules(Base):
    __tablename__ = "t_ds_rules"
    __table_args__ = {"comment": "权限规则组"}

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False, comment="规则名称")
    description: Mapped[Optional[str]] = mapped_column(String(512), comment="描述")
    permission_list: Mapped[Optional[str]] = mapped_column(Text, comment="权限ID列表(JSON)")
    user_list: Mapped[Optional[str]] = mapped_column(Text, comment="用户ID列表(JSON)")
    white_list_user: Mapped[Optional[str]] = mapped_column(Text, comment="白名单用户")
    enable: Mapped[Optional[bool]] = mapped_column(Boolean, default=True, comment="是否启用")
    create_time: Mapped[Optional[datetime.datetime]] = mapped_column(
        TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), comment="创建时间"
    )
    oid: Mapped[Optional[int]] = mapped_column(BigInteger, comment="OID")

class TDsPermission(Base):
    __tablename__ = "t_ds_permission"
    __table_args__ = {"comment": "数据权限详情"}

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[Optional[str]] = mapped_column(String(128), comment="权限名称")
    type: Mapped[str] = mapped_column(String(64), nullable=False, comment="权限类型: row, column")
    ds_id: Mapped[Optional[int]] = mapped_column(BigInteger, comment="数据源ID")
    table_id: Mapped[Optional[int]] = mapped_column(BigInteger, comment="表ID")
    expression_tree: Mapped[Optional[str]] = mapped_column(Text, comment="行权限表达式树(JSON)")
    permissions: Mapped[Optional[str]] = mapped_column(Text, comment="列权限配置(JSON)")
    white_list_user: Mapped[Optional[str]] = mapped_column(Text, comment="白名单用户")
    enable: Mapped[Optional[bool]] = mapped_column(Boolean, default=True, comment="是否启用")
    create_time: Mapped[Optional[datetime.datetime]] = mapped_column(
        TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), comment="创建时间"
    )
    auth_target_type: Mapped[Optional[str]] = mapped_column(String(128), comment="授权目标类型")
    auth_target_id: Mapped[Optional[int]] = mapped_column(BigInteger, comment="授权目标ID")