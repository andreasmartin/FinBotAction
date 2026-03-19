from secrets import token_hex

from app.domain.account_record import AccountRecord
from app.application.repositories.account_record_repository import AccountRecordRepository


class AccountRecordService:
    def __init__(self, repository: AccountRecordRepository):
        self.repository = repository

    def create_account_record(
        self,
        kassier_date: str,
        kassier_name: str,
        praesidium_date: str,
        praesidium_name: str,
        verein_email: str,
    ) -> AccountRecord:
        record = AccountRecord(
            antrags_nr=token_hex(6),
            kassier_date=kassier_date,
            kassier_name=kassier_name,
            praesidium_date=praesidium_date,
            praesidium_name=praesidium_name,
            verein_email=verein_email,
        )
        return self.repository.create(record)

    def list_account_records(self) -> list[AccountRecord]:
        return self.repository.list_all()
