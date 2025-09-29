# 本地开发用的 dify_plugin 模拟模块
from typing import Any, Generator, Dict, List
from abc import ABC, abstractmethod

class ToolInvokeMessage:
    def __init__(self, type: str, message: str = "", meta: Dict = None, blob: bytes = None):
        self.type = type
        self.message = message
        self.meta = meta or {}
        self.blob = blob

class Tool(ABC):
    def __init__(self, **kwargs):
        pass
    
    @abstractmethod
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        pass
    
    def create_text_message(self, text: str) -> ToolInvokeMessage:
        return ToolInvokeMessage("text", text)
    
    def create_blob_message(self, blob: bytes, meta: Dict = None) -> ToolInvokeMessage:
        return ToolInvokeMessage("blob", blob=blob, meta=meta or {})

class Plugin:
    def __init__(self, **kwargs):
        pass

class DifyPluginEnv:
    def __init__(self, **kwargs):
        pass

