from fastapi import APIRouter
from src.app.adapters.entrypoints.api.v1 import route_student, route_login, route_user

api_router = APIRouter()
api_router.include_router(route_user.router, prefix="/user", tags=["user"])
api_router.include_router(route_login.router, prefix="/login", tags=["login"])
api_router.include_router(route_student.router, prefix="/student", tags=["student"])
