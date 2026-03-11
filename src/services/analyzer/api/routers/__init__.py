from fastapi import APIRouter

from .download_report import router as download_router
from .export_report import router as export_router
from .get_task_status import router as status_router


router = APIRouter(prefix="/public/report", tags=["public", "report"])

router.include_router(download_router)
router.include_router(export_router)
router.include_router(status_router)
