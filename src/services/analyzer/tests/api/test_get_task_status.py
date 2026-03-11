from unittest.mock import MagicMock
from src.services.analyzer.api.routers.get_task_status import get_async_result
from src.fastapi_app import app

async def test_get_task_status_success(async_client):
    mock_result = MagicMock()
    mock_result.status = "SUCCESS"

    app.dependency_overrides[get_async_result] = lambda: mock_result

    response = await async_client.get("public/report/status/test_id")

    assert response.status_code == 200
    assert response.json()["status"] == "SUCCESS"
    assert "download_url" in response.json()


async def test_get_task_status_failure(async_client):
    mock_result = MagicMock()
    mock_result.status = "FAILURE"
    mock_result.info = "Something went wrong"

    app.dependency_overrides[get_async_result] = lambda: mock_result

    response = await async_client.get("public/report/status/test_id")

    assert response.status_code == 200
    assert response.json()["status"] == "FAILURE"
    assert response.json()["error"] == "Something went wrong"
