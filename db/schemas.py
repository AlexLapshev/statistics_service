import datetime
from typing import Optional

from pydantic import BaseModel, condecimal, root_validator


class StatisticSchema(BaseModel):
    date: datetime.date
    views: Optional[int] = 0
    clicks: Optional[int] = 0
    cost: Optional[condecimal(decimal_places=2)] = 0.00

    @root_validator(pre=True)
    def validate_values(cls, values):
        for v in ["clicks", "views", "cost"]:
            values[v] = values[v] if values[v] is not None else 0
        return values


class StatisticAggregatedSchema(BaseModel):
    date: datetime.date
    clicks: int
    views: int
    cost: condecimal(decimal_places=2)
    cpc: condecimal(decimal_places=2)
    cpm: condecimal(decimal_places=2)
