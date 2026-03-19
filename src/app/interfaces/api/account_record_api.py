from html import escape
from urllib.parse import parse_qs

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, ValidationError

from app.application.account_record_use_cases import AccountRecordService


class AccountRecordCreateResponse(BaseModel):
    AntragsNr: str


class AccountRecordPayload(BaseModel):
    KassierDate: str
    KassierName: str
    PraesidiumDate: str
    PraesidiumName: str
    VereinEmail: str


class AccountRecordResponse(BaseModel):
    AntragsNr: str
    KassierDate: str
    KassierName: str
    PraesidiumDate: str
    PraesidiumName: str
    VereinEmail: str


router = APIRouter(tags=["account-records"])


def get_service() -> AccountRecordService:
    raise NotImplementedError("Service must be provided via dependency_overrides")


EXAMPLE_PAYLOAD = {
    "KassierDate": "20.05.1980",
    "KassierName": "Monika Meier",
    "PraesidiumDate": "15.02.1980",
    "PraesidiumName": "Hans Muster",
    "VereinEmail": "info@shindokan.ch",
}


POST_OPENAPI_EXTRA = {
    "requestBody": {
        "required": True,
        "content": {
            "application/json": {
                "schema": AccountRecordPayload.model_json_schema(),
                "example": EXAMPLE_PAYLOAD,
            },
            "application/x-www-form-urlencoded": {
                "schema": AccountRecordPayload.model_json_schema(),
                "example": EXAMPLE_PAYLOAD,
            },
            "multipart/form-data": {
                "schema": AccountRecordPayload.model_json_schema(),
                "example": EXAMPLE_PAYLOAD,
            },
        },
    }
}


@router.post(
    "/account-records",
    response_model=AccountRecordCreateResponse,
    status_code=201,
    openapi_extra=POST_OPENAPI_EXTRA,
)
async def create_account_record(request: Request, service: AccountRecordService = Depends(get_service)):
    content_type = request.headers.get("content-type", "")
    raw_payload: dict

    if "application/json" in content_type:
        raw_payload = await request.json()
    elif "application/x-www-form-urlencoded" in content_type:
        encoded = (await request.body()).decode("utf-8")
        parsed = parse_qs(encoded, keep_blank_values=True)
        raw_payload = {key: values[-1] for key, values in parsed.items()}
    elif "multipart/form-data" in content_type:
        form = await request.form()
        raw_payload = dict(form)
    else:
        raw_payload = {}

    try:
        payload = AccountRecordPayload.model_validate(raw_payload)
    except ValidationError:
        raise HTTPException(status_code=400, detail="Missing required fields")

    record = service.create_account_record(
        kassier_date=payload.KassierDate,
        kassier_name=payload.KassierName,
        praesidium_date=payload.PraesidiumDate,
        praesidium_name=payload.PraesidiumName,
        verein_email=payload.VereinEmail,
    )
    return AccountRecordCreateResponse(AntragsNr=record.antrags_nr)


@router.get("/account-records", response_model=list[AccountRecordResponse])
def list_account_records(service: AccountRecordService = Depends(get_service)):
    records = service.list_account_records()
    return [
        AccountRecordResponse(
            AntragsNr=record.antrags_nr,
            KassierDate=record.kassier_date,
            KassierName=record.kassier_name,
            PraesidiumDate=record.praesidium_date,
            PraesidiumName=record.praesidium_name,
            VereinEmail=record.verein_email,
        )
        for record in records
    ]


@router.get("/", response_class=HTMLResponse, include_in_schema=False)
def list_records_page(service: AccountRecordService = Depends(get_service)):
    rows = []
    for record in service.list_account_records():
        rows.append(
            "<li>"
            f"{escape(record.antrags_nr)} | "
            f"{escape(record.kassier_date)} | "
            f"{escape(record.kassier_name)} | "
            f"{escape(record.praesidium_date)} | "
            f"{escape(record.praesidium_name)} | "
            f"{escape(record.verein_email)}"
            "</li>"
        )
    items = "".join(rows)
    return HTMLResponse(f"<html><body><h1>FinBotAction</h1><ul>{items}</ul></body></html>")
