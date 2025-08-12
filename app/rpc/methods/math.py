from pydantic import BaseModel
from app.rpc.registry import registry

class AddParams(BaseModel):
    a: float
    b: float

@registry.method("math.add")
def add(params: AddParams) -> float:
    return params.a + params.b
