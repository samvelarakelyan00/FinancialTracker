from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    server_host: str = '127.0.0.1'
    server_port: int = 8000
    database_url: str = "postgresql://postgres:password@localhost/fintrack"
    jwt_secret: str = "secret"
    jwt_algorithm: str = "HS256"


settings = Settings(
    _env_file='.env',
    _env_file_encoding='utf-8'
)
