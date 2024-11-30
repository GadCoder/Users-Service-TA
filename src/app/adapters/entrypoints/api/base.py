from fastapi import APIRouter
from src.app.adapters.entrypoints.api.v1 import route_admin
from src.app.adapters.entrypoints.api.v1 import route_teacher
from src.app.adapters.entrypoints.api.v1 import route_student

api_router = APIRouter()
api_router.include_router(route_admin.router, prefix="/admin", tags=["admin"])
api_router.include_router(route_student.router, prefix="/students", tags=["students"])
api_router.include_router(route_teacher.router, prefix="/teachers", tags=["teachers"])
