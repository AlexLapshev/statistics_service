import datetime
from typing import Optional


class CrudHelperMixin:
    @staticmethod
    def create_statistics_date_filter_query(from_date: Optional[datetime.date],
                                            to_date: Optional[datetime.date]) -> str:
        raw_sql = """select total_statistics, views, clicks, cost, round(coalesce(cost / nullif (clicks, 0), 0), 2) as cpc, round(coalesce(cost / nullif (views, 0) * 1000, 0), 2) as cpm  
        from (select sum(views) as views, sum(clicks) as clicks, sum(cost) as cost, count(*) as total_statistics
        from "statistics" s 
        where is_active=true and {}
        as _"""
        if not to_date:
            to_date = datetime.date.today()
        if not from_date:
            additional_string = f"date <= '{to_date}') "
        else:
            additional_string = f"date between '{from_date}' and '{to_date}') "
        return raw_sql.format(additional_string)
