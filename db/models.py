from sqlalchemy import Column, Integer, Date, DECIMAL, Boolean

from db.base import Base


class Statistic(Base):
    __tablename__ = "statistics"

    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False, index=True, unique=True)
    views = Column(Integer, nullable=False, default=0)
    clicks = Column(Integer, nullable=False, default=0)
    cost = Column(DECIMAL(10, 2), nullable=False, default=0.00)
    is_active = Column(Boolean, nullable=False, default=True, index=True)
