import datetime

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import Config

engine = create_engine(Config.db_uri())

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Order(Base):
    __tablename__ = "orders"

    id = sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True)
    order_number = sqlalchemy.Column("order_number", sqlalchemy.Integer)
    delivery_date = sqlalchemy.Column(
        "delivery_date", sqlalchemy.Date, default=datetime.date.today
    )
    cost = sqlalchemy.Column("cost", sqlalchemy.Numeric(10, 2))
    cost_rub = sqlalchemy.Column("cost_rub", sqlalchemy.Numeric(10, 2))
    hash = sqlalchemy.Column("hash", sqlalchemy.String)
    is_message_sent = sqlalchemy.Column(
        "is_message_sent", sqlalchemy.Boolean, default=False
    )


def check_and_create_tables():
    if not engine.has_table(Order.__tablename__):
        Base.metadata.create_all(engine, tables=[Order.__table__])
