from dataclasses import dataclass


@dataclass
class AccountRecord:
    antrags_nr: str
    kassier_date: str
    kassier_name: str
    praesidium_date: str
    praesidium_name: str
    verein_email: str
