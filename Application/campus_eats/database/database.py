from sqlalchemy import create_engine

from config import DB_USER, DB_PASSWORD, DB_HOST, DB_NAME

ENGINE = create_engine(
    f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
)


