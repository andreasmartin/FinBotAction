from fastapi import Depends, FastAPI
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from app.infrastructure.config import API_TITLE, API_VERSION, API_DESCRIPTION
from app.infrastructure.database import get_db
from app.infrastructure.persistence.account_record_repository import SQLAlchemyAccountRecordRepository
from app.application.account_record_use_cases import AccountRecordService
from app.interfaces.api import account_record_api


def create_app(init_db: bool = True) -> FastAPI:
    app = FastAPI(
        title=API_TITLE,
        version=API_VERSION,
        description=API_DESCRIPTION,
    )

    def get_account_record_service(db: Session = Depends(get_db)) -> AccountRecordService:
        repo = SQLAlchemyAccountRecordRepository(db)
        return AccountRecordService(repo)

    app.dependency_overrides[account_record_api.get_service] = get_account_record_service
    app.include_router(account_record_api.router)
    app.mount("/ui", StaticFiles(directory="src/app/infrastructure/web/static", html=True), name="ui")

    @app.get("/health")
    def health_check():
        return {"status": "healthy"}

    if init_db:
        from app.infrastructure.database import init_db as _init_db
        _init_db()

    return app


app = create_app()
