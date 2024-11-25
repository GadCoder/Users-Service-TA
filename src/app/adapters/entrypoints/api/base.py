from fastapi import APIRouter
from src.app.adapters.entrypoints.api.v1 import route_students

api_router = APIRouter()
api_router.include_router(route_students.router, prefix="/students", tags=["students"])
