import datetime
from typing import Optional

from fastapi import APIRouter, Depends
from fastapi.params import Query
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse, Response
from starlette.status import HTTP_200_OK, HTTP_422_UNPROCESSABLE_ENTITY

from db.base import db
from db.crud import StatisticsCrud
from db.schemas import StatisticSchema, StatisticAggregatedSchema

statistics_router = APIRouter(
    prefix="/statistics",
    tags=["statistics"],
)


@statistics_router.get("/")
async def get_statistics(from_date: Optional[datetime.date] = Query(None, alias="from"),
                         to_date: Optional[datetime.date] = Query(None, alias="to"),
                         session: AsyncSession = Depends(db)) -> StatisticAggregatedSchema or JSONResponse:
    statistics = await StatisticsCrud(session).get(from_date, to_date)
    if not statistics:
        return JSONResponse(content={"message": "No statistics found"}, status_code=404)
    return statistics


@statistics_router.post("/")
async def add_statistics(statistic: StatisticSchema, session: AsyncSession = Depends(db)):
    s = await StatisticsCrud(session).add(statistic)
    if not s:
        return JSONResponse(content={"message": f"Statistics already exist for this day: {statistic.date}"},
                            status_code=HTTP_422_UNPROCESSABLE_ENTITY)
    return s


@statistics_router.put("/")
async def reset_statistics(session: AsyncSession = Depends(db)):
    await StatisticsCrud(session).reset()
    return Response(status_code=HTTP_200_OK)
