from fastapi import APIRouter
from app.user import router as user_router
from app.config import settings

api_v1_router = APIRouter()

api_v1_router.include_router(
    user_router,
    prefix=settings.api.v1.user.prefix,
    tags=[settings.api.v1.user.tag]
)


@api_v1_router.get("/hello")
async def hello():
    return {"message": "hello"}
