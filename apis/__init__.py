from fastapi import APIRouter

# from .ping import router as test_router
from .todo import router as todo_routers

router = APIRouter()
# router.include_router(test_router, prefix="/ping", tags=["ping"])
router.include_router(todo_routers, prefix="/todo", tags=["todo"])
