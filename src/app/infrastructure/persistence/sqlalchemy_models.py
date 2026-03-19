from sqlalchemy import Column, Integer, String

from app.infrastructure.database import Base


class AccountRecordModel(Base):
    __tablename__ = "account_records"

    id = Column(Integer, primary_key=True, autoincrement=True)
    antrags_nr = Column(String(12), nullable=False, unique=True)
    kassier_date = Column(String(32), nullable=False)
    kassier_name = Column(String(255), nullable=False)
    praesidium_date = Column(String(32), nullable=False)
    praesidium_name = Column(String(255), nullable=False)
    verein_email = Column(String(255), nullable=False)
