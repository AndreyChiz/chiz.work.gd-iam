from contextlib import asynccontextmanager

from fastapi import FastAPI, APIRouter
from fastapi.responses import ORJSONResponse
from app.database import db_master

from app.config import settings
from app.user import router as user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await db_master.dispose()


app = FastAPI(
    lifespan=lifespan,
    default_response_class=ORJSONResponse,
    root_path=settings.api.prefix,
)


# Routes
# v1
api_v1_router = APIRouter()
app.include_router(
    api_v1_router,
    prefix=settings.api.v1.prefix,
)

#/users
api_v1_router.include_router(
    user_router,
    prefix=settings.api.v1.user.prefix,
    tags=[settings.api.v1.user.tag],
)






@api_v1_router.get("/hello")
async def hello():
    return {"message": "hello"}


@app.get("/")
async def root():
    return {str(db_master.engine.url)}
