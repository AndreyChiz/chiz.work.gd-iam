from contextlib import asynccontextmanager
from fastapi import FastAPI, APIRouter
from fastapi.responses import ORJSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from app.database import db_master
from app.config import settings, BASE_DIR
from app.routers import user_router, auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await db_master.dispose()


app = FastAPI(
    lifespan=lifespan,
    default_response_class=ORJSONResponse,
    root_path=settings.api.prefix,
)

# ===== CORS =====
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== API v1 =====
api_v1_router = APIRouter()

api_v1_router.include_router(
    auth_router,
    prefix=settings.api.v1.auth.prefix,
    tags=[settings.api.v1.auth.tag],
)

api_v1_router.include_router(
    user_router,
    prefix=settings.api.v1.user.prefix,
    tags=[settings.api.v1.user.tag],
)


@api_v1_router.get("/hello")
async def hello():
    return {"message": "hello"}


app.include_router(api_v1_router, prefix=settings.api.v1.prefix)

# ===== FRONTEND =====
frontend_path = BASE_DIR.parent / "frontend"

# Монтируем папку как статику
app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")
