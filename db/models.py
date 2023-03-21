from sqlalchemy import Column, Integer, String, Date, DECIMAL

from db.config import Base


class Statistic(Base):
    __tablename__ = 'statistics'

    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False, index=True)
    views = Column(Integer, nullable=True)
    clicks = Column(String, nullable=True)
    cost = Column(DECIMAL(10, 2), nullable=True)
