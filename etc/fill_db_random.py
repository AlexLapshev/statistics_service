import asyncio
import datetime
import random
from _decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession

from db.base import PostgresDatabase
from db.crud import StatisticsCrud
from db.schemas import StatisticsSchema
from tests.test_main import FIRST_DAY


async def insert_100_statistics(session: AsyncSession) -> None:
    random_days = []
    random_day = random.randint(1, 365)
    for i in range(1, 101):
        while random_day in random_days:
            random_day = random.randint(1, 365)
        random_days.append(random_day)
        s = StatisticsSchema(
            date=FIRST_DAY + datetime.timedelta(days=random_day),
            views=random.randint(1000, 2000),
            clicks=random.randint(100, 200),
            cost=Decimal(f"{random.randint(100, 2000)}.{random.randint(1, 99)}"),
        )
        try:
            await StatisticsCrud(session).add(s)
        except Exception as e:
            if "ix_statistics_date" in e.args[0]:
                raise Exception("DATES SHOULD BE UNIQUE, RESET THE DATABASE")
            raise e

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