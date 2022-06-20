from fastapi import APIRouter
from .todo import router as todo_routers

router = APIRouter()
router.include_router(todo_routers, prefix="/todo", tags=["todo"])
