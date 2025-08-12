from fastapi import FastAPI
from app.core.config import settings
from app.core.logging import setup_logging
from app.rpc.transport import router as rpc_router
import app.rpc.methods

def create_app() -> FastAPI:
    setup_logging()
    app = FastAPI(title=settings.APP_NAME)
    app.include_router(rpc_router, prefix=settings.RPC_PATH)
    return app

app = create_app()
