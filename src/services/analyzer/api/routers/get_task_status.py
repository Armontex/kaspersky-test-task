from fastapi import status, APIRouter, Depends
from celery.result import AsyncResult
from src.celery_app import celery_app


router = APIRouter()


def get_async_result(task_id: str) -> AsyncResult:
    return AsyncResult(task_id, app=celery_app)


@router.get(path="/status/{task_id}", status_code=status.HTTP_200_OK)
async def get_task_status(
    task_id: str, result: AsyncResult = Depends(get_async_result)
):
    response = {
        "task_id": task_id,
        "status": result.status,
    }

    if result.status == "SUCCESS":
        response["download_url"] = f"/public/report/download/{task_id}"

    elif result.status == "FAILURE":
        response["error"] = str(result.info)

    return response
