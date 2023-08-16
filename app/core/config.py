from pydantic import BaseSettings


class Settings(BaseSettings):
    app_title: str = 'Благотворительный проект'
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    secret: str = 'SECRET4362'

    class Config:
        env_file = '.env'


settings = Settings()
