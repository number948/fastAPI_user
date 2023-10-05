"""
core configuration for api
"""
from functools import lru_cache
from pydantic import BaseSettings, Field, PostgresDsn, Required
from dotenv import load_dotenv

from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    # database env variables
    DB_USER: str = Field(default=Required, env='DB_USER')
    DB_PASSWORD: str = Field(default=Required, env='DB_PASSWORD')
    DB_SERVER: str = Field(default=Required, env='DB_SERVER')
    DB_PORT: str = Field(default=Required, env='DB_PORT')
    DB_NAME: str = Field(default=Required, env='DB_NAME')

    def assemble_db_connection(self) -> str:
        """
        function that returns the postgres db connection string
        :return: connection string
        :rtype: str
        """
        url: str = PostgresDsn.build(
            scheme="postgresql",
            user=self.DB_USER,
            password=self.DB_PASSWORD,
            host=self.DB_SERVER,
            port=self.DB_PORT,
            path=f"/{self.DB_NAME or ''}",
        )
        return url

    def get_db_url(self) -> str:
        """
        get database url
        :return: database url
        :rtype: str
        """
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_SERVER}:{self.DB_PORT}/{self.DB_NAME}"


@lru_cache
def get_settings() -> Settings:
    """
    get settings from environment variables
    :return: settings
    :rtype: BaseSettings
    """
    return Settings()
