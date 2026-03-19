from abc import ABC, abstractmethod

from app.domain.account_record import AccountRecord


class AccountRecordRepository(ABC):
    @abstractmethod
    def create(self, record: AccountRecord) -> AccountRecord: ...

    @abstractmethod
    def list_all(self) -> list[AccountRecord]: ...
