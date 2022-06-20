from fastapi import FastAPI
from apis.todo import router as todo_router

app = FastAPI(title="Todo API", description="Todo API using FastAPI", version="0.2.0")

app.include_router(todo_router, prefix="/todo", tags=["todo"])

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True)
