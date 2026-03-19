from typing import Dict

from app.domain.account_record import AccountRecord
from app.application.repositories.account_record_repository import AccountRecordRepository


class FakeAccountRecordRepository(AccountRecordRepository):
    def __init__(self):
        self._storage: Dict[str, AccountRecord] = {}

    def create(self, record: AccountRecord) -> AccountRecord:
        new_record = AccountRecord(
            antrags_nr=record.antrags_nr,
            kassier_date=record.kassier_date,
            kassier_name=record.kassier_name,
            praesidium_date=record.praesidium_date,
            praesidium_name=record.praesidium_name,
            verein_email=record.verein_email,
        )
        self._storage[new_record.antrags_nr] = new_record
        return new_record

    def list_all(self) -> list[AccountRecord]:
        return list(self._storage.values())
