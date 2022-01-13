from fastapi import FastAPI

from .database import setup_database
from .routers import setup_router


app = FastAPI()

setup_database(app)
setup_router(app)
