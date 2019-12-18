import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or b'\x08\x0e_\xb8\x94]\xacL\x13N\xedVD\xba\xfd\x85'
    PG_USER = "project1"
    PG_PASSWORD = "password"
    PG_HOST = "localhost"
    PG_PORT = 5432
    DB_NAME = "project1_db"
    SQLALCHEMY_DATABASE_URI = f"postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


configs = {
    # "TEST": TestConfig,
    "DEFAULT": Config
}

def get_config(env):
    return configs.get(env)