import datetime
from typing import Optional, Literal

from sqlalchemy import update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from db.helpers import CrudHelperMixin
from db.models import Statistic
from db.schemas import StatisticsSchema


class StatisticsCrud:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get(
        self,
        from_date: Optional[datetime.date],
        to_date: Optional[datetime.date],
        order_by: Literal[
            "date",
            "clicks",
            "views",
            "cost",
        ] = "date",
        order: Literal["asc", "desc"] = "asc",
    ) -> Optional[list[StatisticsSchema]]:
        q = CrudHelperMixin.create_statistics_date_filter_query(
            from_date, to_date, order_by, order
        )
        statistics = await self.db_session.execute(q)
        statistics = statistics.scalars().all()
        return [
            StatisticsSchema(
                views=s.views, cost=s.cost, date=s.date, clicks=s.clicks
            )  # noqa
            for s in statistics
        ]

    async def add(
        self, statistic: StatisticsSchema
    ) -> Optional[StatisticsSchema]:  # noqa
        new_s = Statistic(
            date=statistic.date,
            views=statistic.views,
            cost=statistic.cost,
            clicks=statistic.clicks,
        )
        self.db_session.add(new_s)
        try:
            await self.db_session.flush()
        except IntegrityError:
            return None
        return statistic

    async def reset(self):
        q = update(Statistic).values(is_active=False)
        q = await self.db_session.execute(q)
        return q
