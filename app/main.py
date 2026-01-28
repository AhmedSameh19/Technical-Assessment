from fastapi import FastAPI

from app.api.router import api_router
from app.db.database import engine


app = FastAPI(title="Technical Assessment")



app.include_router(api_router)


