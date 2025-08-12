from typing import Any, Callable, Dict, Optional
from fastapi import Depends
from app.deps.auth import AuthContext, auth_dependency

class Registry:
    def __init__(self):
        self._methods: Dict[str, Callable[..., Any]] = {}

    def method(self, name: Optional[str] = None):
        def deco(fn: Callable[..., Any]):
            self._methods[name or fn.__name__] = fn
            return fn
        return deco

    def get(self, name: str) -> Callable[..., Any]:
        if name not in self._methods:
            raise KeyError(name)
        return self._methods[name]

registry = Registry()

# Optional per-method wrapper if you want auth injected:
def with_auth(fn: Callable[..., Any]):
    def wrapper(*args, auth: AuthContext = Depends(auth_dependency), **kwargs):
        return fn(*args, auth=auth, **kwargs)
    return wrapper
