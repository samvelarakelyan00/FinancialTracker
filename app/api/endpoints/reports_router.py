from typing import Any, List

# FastAPI
from fastapi import APIRouter, Depends, UploadFile, File, BackgroundTasks
from fastapi.responses import StreamingResponse

from services.reports import ReportsService
from schemas.auth_schemas import User
from services.auth import get_current_user

router = APIRouter(
    prefix='/reports',
    tags=["Reports"]
)


@router.post("/import-from-csv")
def import_from_csv(
        background_tasks: BackgroundTasks,
        file: UploadFile = File(...),
        user: User = Depends(get_current_user),
        service: ReportsService = Depends()):

    background_tasks.add_task(
        service.import_from_csv,
        user.user_id,
        file.file
    )

    # service.import_from_csv(user_id=user.user_id, file=file)


@router.get('/export-to-csv')
def export_to_csv(user_id: int,
                  service: ReportsService = Depends()):

    report = service.export_to_csv(user_id=user_id)

    return StreamingResponse(
        report,
        media_type='text/csv',
        headers={
            "Content-Disposition": "attachment; filename=report.csv"
        },
    )
