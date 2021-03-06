from fastapi import APIRouter

from .auth import router as auth_router
from .todo import router as todo_router

router = APIRouter()

router.include_router(todo_router, prefix="/todo", tags=["todo"])
router.include_router(auth_router, prefix="/auth", tags=["auth"])
