from typing import Union

import uvicorn as uvicorn
from fastapi import FastAPI, Depends

from db.config import engine, Base, async_session
from db.crud import StatisticsCrud
from db.schemas import StatisticSchema

app = FastAPI()


@app.get("/")
async def read_root():
    async with async_session() as session:
        async with session.begin():
            await StatisticsCrud(session).get_statistic(1)
    return {"Hello": "World"}


@app.post("/statistics/")
async def create_item(statistic: StatisticSchema, s: Depends()):
    return statistic

# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}


if __name__ == '__main__':
    uvicorn.run(app=app, port=8000, host='0.0.0.0')
