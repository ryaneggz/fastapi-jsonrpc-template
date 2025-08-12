from typing import Any, Literal, Optional, Union, List
from pydantic import BaseModel, Field

JsonValue = Union[dict, list, str, int, float, bool, None]

class Error(BaseModel):
    code: int
    message: str
    data: Optional[JsonValue] = None

class Request(BaseModel):
    jsonrpc: Literal["2.0"] = "2.0"
    method: str
    params: Optional[Union[list[Any], dict[str, Any]]] = None
    id: Optional[Union[str, int]] = None  # None => notification

class Response(BaseModel):
    jsonrpc: Literal["2.0"] = "2.0"
    result: Optional[JsonValue] = None
    error: Optional[Error] = None
    id: Optional[Union[str, int]] = None

Batch = List[Request]
