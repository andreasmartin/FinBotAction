from app.application.account_record_use_cases import AccountRecordService
from fake_repository import FakeAccountRecordRepository


def test_create_account_record_returns_generated_antrags_nr():
    repo = FakeAccountRecordRepository()
    svc = AccountRecordService(repo)

    record = svc.create_account_record(
        kassier_date="20.05.1980",
        kassier_name="Monika Meier",
        praesidium_date="15.02.1980",
        praesidium_name="Hans Muster",
        verein_email="info@shindokan.ch",
    )
    assert len(record.antrags_nr) == 12


def test_list_account_records_returns_created_records():
    repo = FakeAccountRecordRepository()
    svc = AccountRecordService(repo)

    svc.create_account_record(
        kassier_date="20.05.1980",
        kassier_name="Monika Meier",
        praesidium_date="15.02.1980",
        praesidium_name="Hans Muster",
        verein_email="info@shindokan.ch",
    )
    svc.create_account_record(
        kassier_date="21.05.1980",
        kassier_name="Petra Baum",
        praesidium_date="16.02.1980",
        praesidium_name="Paul Vogel",
        verein_email="verein@example.ch",
    )

    records = svc.list_account_records()
    assert len(records) == 2
