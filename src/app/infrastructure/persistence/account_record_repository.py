from sqlalchemy.orm import Session

from app.domain.account_record import AccountRecord
from app.infrastructure.persistence.sqlalchemy_models import AccountRecordModel
from app.application.repositories.account_record_repository import AccountRecordRepository


class SQLAlchemyAccountRecordRepository(AccountRecordRepository):
    def __init__(self, session: Session):
        self.session = session

    def create(self, record: AccountRecord) -> AccountRecord:
        model = AccountRecordModel(
            antrags_nr=record.antrags_nr,
            kassier_date=record.kassier_date,
            kassier_name=record.kassier_name,
            praesidium_date=record.praesidium_date,
            praesidium_name=record.praesidium_name,
            verein_email=record.verein_email,
        )
        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)
        return self._to_entity(model)

    def list_all(self) -> list[AccountRecord]:
        models = self.session.query(AccountRecordModel).order_by(AccountRecordModel.id.asc()).all()
        return [self._to_entity(m) for m in models]

    @staticmethod
    def _to_entity(model: AccountRecordModel) -> AccountRecord:
        return AccountRecord(
            antrags_nr=model.antrags_nr,
            kassier_date=model.kassier_date,
            kassier_name=model.kassier_name,
            praesidium_date=model.praesidium_date,
            praesidium_name=model.praesidium_name,
            verein_email=model.verein_email,
        )
