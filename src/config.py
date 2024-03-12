from pydantic_settings import SettingsConfigDict, BaseSettings


class Settings(BaseSettings):
    neo4j_url: str
    neo4j_user: str
    neo4j_password: str
    redis_url: str

    model_config = SettingsConfigDict(env_file=".env", extra="allow")


settings = Settings()
