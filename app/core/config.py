from typing import Optional
from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    app_title: str = 'Благотворительный проект'
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    secret: str = 'SECRET4362'
    first_superuser_email: Optional[EmailStr] = 'zhitnikoveg@yandex.ru'
    first_superuser_password: Optional[str] = 'Pass2020!'

    class Config:
        env_file = '.env'


settings = Settings()
