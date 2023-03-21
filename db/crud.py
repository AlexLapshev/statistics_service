import datetime
from _decimal import Decimal
from typing import Optional

from sqlalchemy import update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncConnection
from sqlalchemy.sql import text

from db.helpers import CrudHelperMixin
from db.models import Statistic
from db.schemas import StatisticSchema, StatisticAggregatedSchema


class StatisticsCrud:
    def __init__(self, db_session):
        self.db_session: AsyncConnection = db_session

    async def get(self,
                  from_date: Optional[datetime.date],
                  to_date: Optional[datetime.date]) -> Optional[StatisticAggregatedSchema]:
        q = text(CrudHelperMixin.create_statistics_date_filter_query(from_date, to_date))
        q = await self.db_session.execute(q)
        raw = q.fetchone()
        if raw.total_statistics == 0:
            return None
        return StatisticAggregatedSchema(
            date=datetime.date.today(),
            cost=raw.cost,
            clicks=raw.clicks,
            views=raw.views,
            cpc=Decimal(raw.cpc),
            cpm=Decimal(raw.cpm)
        )

    async def add(self, statistic: StatisticSchema) -> Optional[StatisticSchema]:
        new_s = Statistic(date=statistic.date, views=statistic.views, cost=statistic.cost, clicks=statistic.clicks)
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
