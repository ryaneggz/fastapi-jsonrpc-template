from app.rpc.registry import registry

@registry.method("ping")
def ping() -> str:
    return "pong"
