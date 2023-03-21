import datetime
from typing import Optional, Literal

from sqlalchemy import select, Select

from db.models import Statistic


class CrudHelperMixin:
    @staticmethod
    def create_statistics_date_filter_query(
        from_date: Optional[datetime.date],
        to_date: Optional[datetime.date],
        order_by: Literal[
            "date",
            "clicks",
            "views",
            "cost",
        ] = "date",
        order: Literal["asc", "desc"] = "asc",
    ) -> Select:
        if not to_date:
            to_date = datetime.date.today()
        if from_date:
            q = (
                select(Statistic)
                .filter(Statistic.date.between(from_date, to_date))
                .where(Statistic.is_active == True)  # noqa
            )
        else:
            q = (
                select(Statistic)
                .where(Statistic.date <= to_date)
                .where(Statistic.is_active == True)  # noqa
            )
        if order == "asc":
            q = q.order_by(getattr(Statistic, order_by).asc())
        else:
            q = q.order_by(getattr(Statistic, order_by).desc())
        return q
