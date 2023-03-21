import datetime

from pydantic import BaseModel, condecimal


class StatisticSchema(BaseModel):
    date: datetime.date
    views: int | None = None
    clicks: int | None = None
    cost: condecimal(decimal_places=2)
