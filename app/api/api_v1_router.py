from fastapi import APIRouter

api_v1_router = APIRouter()


@api_v1_router.get("/hello")
async def hello():
    return {'message': 'hello'}    
