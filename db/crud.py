from sqlalchemy.ext.asyncio import AsyncConnection
from sqlalchemy.future import select

from db.models import Statistic


class StatisticsCrud:
    def __init__(self, db_session):
        self.db_session: AsyncConnection = db_session

    async def get_statistic(self, statistic_id: int):
        q = await self.db_session.execute(select(Statistic).where(Statistic.id == statistic_id))
        return q.scalars().all()

    async def add_statistic(self, name: str, author: str, release_year: int):
        new_book = Book(name=name, author=author, release_year=release_year)
        self.db_session.add(new_book)
        await self.db_session.flush()

    async def create_author(self, full_name: str):
        new_book = Author(full_name=full_name)
        self.db_session.add_all([new_book])
        await self.db_session.flush()
