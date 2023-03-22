from db.schemas import (
    StatisticsSchema,
    StatisticsAggregatedResponseSchema,
    StatisticsAggregatedSchema,
)


class StatisticsAggregator:
    def __init__(self, statistics: list[StatisticsSchema]):
        self.statistics = statistics

    def aggregate(self) -> StatisticsAggregatedResponseSchema:
        total_clicks = sum([s.clicks for s in self.statistics])
        total_views = sum([s.views for s in self.statistics])
        total_cost = sum([s.cost for s in self.statistics])
        average_cpc = total_cost / total_clicks if total_clicks else 0
        average_cpm = total_cost / total_views * 1000 if total_views else 0
        aggregated_one_by_one = self.aggregate_one_by_one()
        return StatisticsAggregatedResponseSchema(
            total_clicks=total_clicks,
            total_views=total_views,
            total_cost=total_cost,
            average_cpc=average_cpc,
            average_cpm=average_cpm,
            statistics=aggregated_one_by_one,
        )

    def aggregate_one_by_one(self) -> list[StatisticsAggregatedSchema]:
        res = []
        for s in self.statistics:
            cpc = s.cost / s.clicks if s.clicks else 0
            cpm = s.cost / s.views * 1000 if s.views else 0
            res.append(StatisticsAggregatedSchema(**s.dict(), cpc=cpc, cpm=cpm))  # noqa
        return res
