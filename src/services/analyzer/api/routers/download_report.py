import os
from typing import Callable
from pathlib import Path
from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.responses import FileResponse
from src.config.settings import settings
from ..const import REPORTS_DIR

router = APIRouter()

IsPathExistsFunc = Callable[[str | Path], bool]
BuildFileResponseFunc = Callable[[str | Path], FileResponse]


def get_is_path_exists() -> IsPathExistsFunc:
    return os.path.exists


def get_build_file_response() -> BuildFileResponseFunc:
    return lambda path: FileResponse(
        path=path,
        filename="analysis_result.xlsx",
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )


@router.get(
    "/download/{task_id}",
    status_code=status.HTTP_200_OK,
    responses={404: {"description": "Файл не найден или еще не готов"}},
)
async def download_report(
    task_id: str,
    is_path_exists: IsPathExistsFunc = Depends(get_is_path_exists),
    build_file_response: BuildFileResponseFunc = Depends(get_build_file_response),
):
    output_path = settings.storage_path / REPORTS_DIR / f"{task_id}.xlsx"

    if not is_path_exists(output_path):
        raise HTTPException(status_code=404, detail="Файл не найден или еще не готов")

    return build_file_response(output_path)
