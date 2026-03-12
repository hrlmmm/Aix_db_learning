import json
import os

from model.db_connection_pool import get_db_pool
from model.db_models import TAiModel

pool = get_db_pool()

# 默认超时时间:30分钟
# 与 deep_research_agent.py 的 DEFAULT_LLM_TIMEOUT 保持一致
# 超时链路：LLM(15min) < TASK(30min) < Sanic RESPONSE(35min) < 前端 fetch(36min)
DEFAULT_LLM_TIMEOUT = int(os.getenv("LLM_TIMEOUT", 30 * 60))


def get_llm(temperature=0.7, timeout=None):
    """
    获取LLM模型
    :param temperature: 模型温度
    :param timeout: 超时时间(秒)

    :return: LLM模型实例
    """

    with pool.get_session() as session:
        # Fetch the default model
        model = (
            session.query(TAiModel)
            .filter(TAiModel.default_model == True, TAiModel.model_type == 1)
            .first()
        )
        if model is None:
            raise Exception("No default AI model configured in database")
        
        # Map supplier to model type string used in map
        # 1:OpenAI, 2:Azure, 3:Ollama, 4:vLLM, 5:DeepSeek, 6:Qwen, 7:Moonshot, 8:ZhipuAI, 9:Other
        supplier = model.supplier

        # 目前统一将 Qwen 也视为通过 OpenAI 协议接入，避免 ChatTongyi 及其 LangSmith/OpenTelemetry 依赖
        if supplier == 3:
            model_type = "ollama"
        else:
            # Default to openai for others (OpenAI, Qwen, DeepSeek, Moonshot, Zhipu, vLLM, etc.)
            model_type = "openai"

        model_name = model.base_model
        model_api_key = model.api_key
        model_base_url = model.api_domain

        try:
            temperature = float(temperature)
        except ValueError:
            temperature = 0.75

        if timeout is None:
            timeout = DEFAULT_LLM_TIMEOUT
        else:
            try:
                timeout = int(timeout)
            except ValueError:
                timeout = DEFAULT_LLM_TIMEOUT
            
        def _get_openai():
            """
            延迟导入 ChatOpenAI,避免在应用启动阶段因 langsmith/opentelemetry 初始化失败导致进程退出。
            如果导入失败，直接抛异常，由上层决定如何处理（通常是显式配置问题）。
            """
            try:
                from langchain.chat_models import ChatOpenAI
            except Exception as e:
                print(
                    f"[ERROR] Failed to import ChatOpenAI, please check langchain-openai/langsmith/opentelemetry installation: {e}"
                )
                raise
            
            return ChatOpenAI(
                model=model_name,
                temperature=temperature,
                api_key=model_api_key,
                base_url=model_base_url or "empty",
                timeout=timeout,
            )

        def _get_ollama():
            """
            延迟导入 ChatOllama,避免在模块加载阶段触发不必要的依赖。
            """
            try:
                from langchain_ollama import ChatOllama
            except Exception as e:
                print(
                    f"[WARN] Failed to import ChatOllama, fallback to ChatOpenAI: {e}"
                )
                return _get_openai()

            return ChatOllama(
                model=model_name,
                temperature=temperature,
                base_url=model_base_url,
                timeout=timeout,  # 设置超时时间（秒）
            )
        
        model_map = {
            "openai": _get_openai,
            "ollama": _get_ollama,
        }
        
        if model_type in model_map:
            return model_map[model_type]()
        else:
            # Should not happen given logic above, but fallback to openai
            return model_map["openai"]()