import asyncio
import datetime
from _decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession

from db.base import PostgresDatabase
from db.crud import StatisticsCrud
from db.schemas import StatisticsSchema
from tests.test_main import FIRST_DAY


async def insert_100_statistics(session: AsyncSession) -> None:
    d = FIRST_DAY
    for i in range(1, 100):
        s = StatisticsSchema(
            date=d + datetime.timedelta(days=i),
            views=100,
            clicks=100,
            cost=Decimal(100),
        )
        await StatisticsCrud(session).add(s)
    s = StatisticsSchema(
        date=d + datetime.timedelta(days=100),
        views=37,
        clicks=37,
        cost=Decimal("37.84"),
    )
    await StatisticsCrud(session).add(s)
    await session.commit()
    print("SUCCESSFULLY INSERTED 100 STATISTICS")


async def main(postgres_db: PostgresDatabase):
    async_gen_session = postgres_db()
    session = await anext(async_gen_session)
    await insert_100_statistics(session)


if __name__ == "__main__":
    db = PostgresDatabase()
    db.setup(echo=False)
    asyncio.run(main(db))
