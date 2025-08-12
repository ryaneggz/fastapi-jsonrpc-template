from typing import Any, List, Union
from fastapi import APIRouter, Request as HttpRequest
from pydantic import ValidationError, BaseModel
from app.rpc.schema import Request as RpcRequest, Response as RpcResponse, Error as RpcError
from app.rpc.registry import registry
import traceback
import logging
import inspect

log = logging.getLogger(__name__)
router = APIRouter()

# JSON-RPC error codes
PARSE_ERROR = -32700
INVALID_REQUEST = -32600
METHOD_NOT_FOUND = -32601
INVALID_PARAMS = -32602
INTERNAL_ERROR = -32603

def make_error(id: Any, code: int, message: str, data: Any = None) -> RpcResponse:
    return RpcResponse(error=RpcError(code=code, message=message, data=data), id=id)

def handle_call(req: RpcRequest) -> Union[RpcResponse, None]:
    # Notifications (id is None) must produce no output
    is_notification = req.id is None
    try:
        fn = registry.get(req.method)
    except KeyError:
        return None if is_notification else make_error(req.id, METHOD_NOT_FOUND, "Method not found")

    try:
        # Map params
        if req.params is None:
            result = fn()
        elif isinstance(req.params, list):
            result = fn(*req.params)
        elif isinstance(req.params, dict):
            # If method expects a single Pydantic BaseModel param, construct it from the dict
            signature = inspect.signature(fn)
            parameters = list(signature.parameters.values())
            if len(parameters) == 1:
                param = parameters[0]
                annotation = param.annotation
                if (
                    annotation is not inspect._empty
                    and isinstance(annotation, type)
                    and issubclass(annotation, BaseModel)
                ):
                    model_instance = annotation.model_validate(req.params)
                    result = fn(model_instance)
                else:
                    result = fn(**req.params)
            else:
                result = fn(**req.params)
        else:
            return None if is_notification else make_error(req.id, INVALID_PARAMS, "Invalid params")
        return None if is_notification else RpcResponse(result=result, id=req.id)
    except ValidationError as ve:
        return None if is_notification else make_error(req.id, INVALID_PARAMS, "Invalid params", ve.errors())
    except Exception as e:
        log.exception("RPC method error")
        return None if is_notification else make_error(
            req.id, INTERNAL_ERROR, "Internal error", {"type": type(e).__name__, "trace": traceback.format_exc()}
        )

@router.post("")
async def rpc_endpoint(http_request: HttpRequest):
    try:
        payload = await http_request.json()
    except Exception:
        # parsing error cannot include id (unknown)
        return make_error(None, PARSE_ERROR, "Parse error").model_dump()

    # Batch or single
    if isinstance(payload, list):
        responses: List = []
        for item in payload:
            try:
                req = RpcRequest.model_validate(item)
            except ValidationError as ve:
                responses.append(make_error(item.get("id") if isinstance(item, dict) else None,
                                            INVALID_REQUEST, "Invalid Request", ve.errors()).model_dump())
                continue
            resp = handle_call(req)
            if resp is not None:
                responses.append(resp.model_dump())
        # If all were notifications, MUST return an empty body (not [])
        return responses if responses else ""
    else:
        try:
            req = RpcRequest.model_validate(payload)
        except ValidationError as ve:
            return make_error(payload.get("id") if isinstance(payload, dict) else None,
                              INVALID_REQUEST, "Invalid Request", ve.errors()).model_dump()
        resp = handle_call(req)
        return "" if resp is None else resp.model_dump()
