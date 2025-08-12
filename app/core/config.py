from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "jsonrpc"
    RPC_PATH: str = "/rpc"
    DEBUG: bool = False

settings = Settings()  # reads env
