import databases
from fastapi import FastAPI
import sqlalchemy

from .settings import settings

TEST_DB_URL = f"sqlite:///{str(settings.base_dir)}/db/test_db.sqlite"
DB_URL = f"sqlite:///{str(settings.base_dir)}/db/dev_db.sqlite"
# DB_URL = f"postgresql://root:root1234@db:5432/dev_db" # your DB url


def get_db_url():
    if settings.environment == "test":
        return TEST_DB_URL
    return DB_URL


database = databases.Database(get_db_url())
metadata = sqlalchemy.MetaData()


def setup_database(app: FastAPI):
    app.state.database = database

    @app.on_event("startup")
    async def startup() -> None:
        database_ = app.state.database
        if not database_.is_connected:
            await database_.connect()

    @app.on_event("shutdown")
    async def shutdown() -> None:
        database_ = app.state.database
        if database_.is_connected:
            await database_.disconnect()
