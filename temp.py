d = datetime.date.today()
for i in range(1, 100):
    s = StatisticSchema(date=d - datetime.timedelta(days=i), views=randint(1000, 2000), clicks=randint(1000, 2000),
                        cost=Decimal(randint(80, 120)))
    await StatisticsCrud(session).add(s)


d = datetime.date.today()
for i in range(1, 11):
    s = StatisticSchema(date=d - datetime.timedelta(days=i), views=randint(10), clicks=10,
                        cost=Decimal(100))
    await StatisticsCrud(session).add(s)