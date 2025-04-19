from fastapi import FastAPI
from app.api.task_router import router as task_router

app = FastAPI()

app.include_router(task_router)

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI"}
