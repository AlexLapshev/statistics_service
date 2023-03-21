from typing import Union

import uvicorn as uvicorn
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from statistics.router import statistics_router
from db.base import db
from db.crud import StatisticsCrud

app = FastAPI()
app.include_router(statistics_router)


@app.on_event("startup")
async def setup_db() -> None:
    db.setup()


@app.get("/")
async def read_root(session: AsyncSession = Depends(db)):
    a = await StatisticsCrud(session).get_statistic(1)
    return {"Hello": "World"}


# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}


if __name__ == '__main__':
    uvicorn.run(app=app, port=8000, host='0.0.0.0')
