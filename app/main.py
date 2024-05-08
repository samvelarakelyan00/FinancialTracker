# Standard
# ...

# FastAPI
from fastapi import FastAPI

# Own modules
from database import engine
from models import models

from api import router


# models.Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="FinTrack"
)


app.include_router(router)
