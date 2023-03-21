import uvicorn as uvicorn
from fastapi import FastAPI

from services.statistics.router import statistics_router
from db.base import db

app = FastAPI()
app.include_router(statistics_router)


@app.on_event("startup")
async def setup_db() -> None:
    db.setup()


@app.get("/")
async def read_root():
    return {"message": "Hello from statistics service."}


if __name__ == "__main__":
    uvicorn.run(app=app, port=8000, host="0.0.0.0")
