from __future__ import annotations
import uuid
from typing import Callable, Awaitable
from pydantic import BaseModel, ConfigDict
from fastapi import APIRouter, UploadFile, File, status, HTTPException, Depends
from src.config.settings import settings
from ..utils import write_file
from ...app.tasks import analyze_file_task


router = APIRouter()

AnalyzeFileTask = Callable[[str, str], dict[str, str]]
WriteFileFunc = Callable[[str, UploadFile], Awaitable[None]]


class TaskResponseModel(BaseModel):
    task_id: str

    model_config = ConfigDict(json_schema_extra={"task_id": "id"})


def get_analyze_file_task() -> AnalyzeFileTask:
    return analyze_file_task


def get_write_file() -> WriteFileFunc:
    return write_file


@router.post(
    path="/export",
    status_code=status.HTTP_202_ACCEPTED,
    responses={
        500: {"description": "Ошибка при сохранении файла"},
    },
    response_model=TaskResponseModel,
)
async def export_report(
    file: UploadFile = File(...),
    task: AnalyzeFileTask = Depends(get_analyze_file_task),
    write_file: WriteFileFunc = Depends(get_write_file),
):
    task_id = str(uuid.uuid4())

    input_path = settings.storage_path / f"tmp/{task_id}.txt"
    output_path = settings.storage_path / f"tmp/{task_id}.xlsx"

    try:
        await write_file(str(input_path), file)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка при сохранении файла",
        ) from e

    task.delay(str(input_path), str(output_path))
    return TaskResponseModel(task_id=task_id)
