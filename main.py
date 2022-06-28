from fastapi import FastAPI
from apis import router as router
from core.config import Config

RELOAD = Config.RELOAD
HOST = Config.HOST
PORT = Config.PORT

app = FastAPI(title="Todo API", description="Todo API using FastAPI", version="0.2.0")

app.include_router(router, prefix="/api")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=RELOAD, host=HOST, port=PORT)
