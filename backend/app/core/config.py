from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "FortSight AI"
    DATABASE_URL: str = "postgresql://postgres:postgres@db:5432/fortsight"
    DEM_S3_URL: str = "s3://copernicus-dem-30m/Copernicus_DSM_COG_10_N18_00_E073_00_DEM/Copernicus_DSM_COG_10_N18_00_E073_00_DEM.tif"

    class Config:
        env_file = ".env"

settings = Settings()
