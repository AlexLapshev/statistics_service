import datetime
from _decimal import Decimal
from typing import Optional

from pydantic import BaseModel, condecimal, root_validator, validator


class StatisticsSchema(BaseModel):
    date: datetime.date
    views: Optional[int] = 0
    clicks: Optional[int] = 0
    cost: Optional[condecimal(decimal_places=2)] = 0.00

    @root_validator(pre=True)
    def validate_values(cls, values):
        for v in ["clicks", "views"]:
            if hasattr(values[v], "is_integer") and not values[v].is_integer():
                raise ValueError(f"Not acceptable, {v} can't be a number with a floating point.")
            values[v] = values[v] if values[v] is not None else 0
        values["cost"] = values["cost"] if values["cost"] is not None else 0
        return values

    @validator("date")
    def validate_date(cls, date):
        if date > datetime.date.today():
            raise ValueError("Date is greater than today")
        return date


class BaseAggregated(BaseModel):
    @root_validator(pre=True)
    def validate_values(cls, values):
        for k, v in values.items():
            if isinstance(v, Decimal):
                values[k] = round(v, 2)
        return values


class StatisticsAggregatedSchema(BaseAggregated, StatisticsSchema):
    cpc: condecimal(decimal_places=2)
    cpm: condecimal(decimal_places=2)


class StatisticsAggregatedResponseSchema(BaseAggregated):
    total_clicks: int
    total_views: int
    total_cost: condecimal(decimal_places=2)
    average_cpc: condecimal(decimal_places=2)
    average_cpm: condecimal(decimal_places=2)
    statistics: list[StatisticsAggregatedSchema]
