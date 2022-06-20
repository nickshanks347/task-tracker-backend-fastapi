from fastapi import FastAPI
from apis import router as test_router

app = FastAPI()

app.include_router(test_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True)
