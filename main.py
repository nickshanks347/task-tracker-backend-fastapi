try:
    from fastapi import FastAPI
    from apis import router as router

    app = FastAPI(title="Todo API", description="Todo API using FastAPI", version="0.2.0")

    app.include_router(router, prefix="/api")

    if __name__ == "__main__":
        import uvicorn

        uvicorn.run("main:app", reload=True)
except FileNotFoundError:
    print("Config file not found...")
    print("Please ensure config.yaml exists in the data directory...")
    exit(1)
