from fastapi import FastAPI
from app.database import db_master

app = FastAPI()


@app.get("/")
async def root():
    return {str(db_master.engine.url)}
