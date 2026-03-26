from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

    APP_NAME: str = 'Enterprise CRM ERP'
    APP_VERSION: str = '0.1.0'
    API_PREFIX: str = '/api/v1'

    SECRET_KEY: str = Field(default='change-me-in-production', min_length=16)
    ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    MSSQL_SERVER: str = 'localhost'
    MSSQL_PORT: int = 1433
    MSSQL_DATABASE: str = 'crm_erp'
    MSSQL_USERNAME: str = 'sa'
    MSSQL_PASSWORD: str = 'Your_strong_Password123'
    MSSQL_DRIVER: str = 'ODBC Driver 18 for SQL Server'
    SQL_ECHO: bool = False

    @property
    def sqlalchemy_database_uri(self) -> str:
        driver = self.MSSQL_DRIVER.replace(' ', '+')
        return (
            f"mssql+pyodbc://{self.MSSQL_USERNAME}:{self.MSSQL_PASSWORD}"
            f"@{self.MSSQL_SERVER}:{self.MSSQL_PORT}/{self.MSSQL_DATABASE}"
            f"?driver={driver}&TrustServerCertificate=yes"
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()
