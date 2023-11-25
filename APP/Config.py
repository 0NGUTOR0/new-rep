from pydantic import BaseSettings

class Settings(BaseSettings):
    database_password : str = "postg"
    database_hostname : str = "localhost"
    database_username: str = "postgres"
    database_name: str ="NEWAPI DB"
    database_port: str = "5432"
    secret_key : str ="09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    algorithm: str  = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES : int = 60
    
    class Config:
        env_file = ".env"

settings = Settings()

print(settings.database_password)