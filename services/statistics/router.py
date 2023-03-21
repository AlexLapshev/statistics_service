import datetime
from typing import Optional, Literal

from fastapi import APIRouter, Depends
from fastapi.params import Query
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse, Response
from starlette.status import HTTP_200_OK, HTTP_422_UNPROCESSABLE_ENTITY, HTTP_404_NOT_FOUND

from db.base import db
from db.crud import StatisticsCrud
from db.schemas import StatisticsSchema, StatisticsAggregatedResponseSchema
from services.statistics.helpers import StatisticsAggregator

statistics_router = APIRouter(
    prefix="/statistics",
    tags=["statistics"],
)


@statistics_router.get("/")
async def get_statistics(
        from_date: Optional[datetime.date] = Query(None, alias="from"),
        to_date: Optional[datetime.date] = Query(None, alias="to"),
        order_by: Literal[
            "date",
            "clicks",
            "views",
            "cost",
        ] = "date",
        order: Literal["asc", "desc"] = "asc",
        session: AsyncSession = Depends(db),
) -> StatisticsAggregatedResponseSchema or JSONResponse:
    statistics = await StatisticsCrud(session).get(from_date, to_date, order_by, order)  # noqa
    if not statistics:
        return JSONResponse(content={"message": "No statistics found"}, status_code=HTTP_404_NOT_FOUND)  # noqa
    aggregated_statistics = StatisticsAggregator(statistics).aggregate()
    return aggregated_statistics


@statistics_router.post("/")
async def add_statistics(
        statistic: StatisticsSchema, session: AsyncSession = Depends(db)
) -> JSONResponse or StatisticsSchema:
    s = await StatisticsCrud(session).add(statistic)
    if not s:
        return JSONResponse(
            content={
                "message": f"Statistics already exist for this day: {statistic.date}"  # noqa
            },
            status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        )
    return s


@statistics_router.put("/")
async def reset_statistics(session: AsyncSession = Depends(db)) -> Response:
    await StatisticsCrud(session).reset()
    return Response(status_code=HTTP_200_OK)
