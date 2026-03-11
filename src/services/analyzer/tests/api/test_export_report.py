import pytest
from unittest.mock import MagicMock, AsyncMock
from httpx import AsyncClient
from src.fastapi_app import app
from src.services.analyzer.api.routers.export_report import (
    get_analyze_file_task,
    get_write_file,
)
from src.config.settings import settings


@pytest.fixture(autouse=True)
def override_settings(tmp_path):
    old_path = settings.storage_path
    settings.storage_path = tmp_path
    yield
    settings.storage_path = old_path


async def test_export_report_success(async_client: AsyncClient):
    mock_task = MagicMock()
    mock_write = AsyncMock()

    app.dependency_overrides[get_analyze_file_task] = lambda: mock_task
    app.dependency_overrides[get_write_file] = lambda: mock_write

    file_data = {"file": ("test.txt", b"hello world", "text/plain")}

    response = await async_client.post("public/report/export", files=file_data)
    assert response.status_code == 202

    task_id = response.json()["task_id"]

    mock_task.apply_async.assert_called_once()

    _, kwargs = mock_task.apply_async.call_args

    assert kwargs["task_id"] == task_id

    actual_task_args = kwargs.get("args", [])

    assert any("tasks" in str(arg) for arg in actual_task_args)
    assert any("reports" in str(arg) for arg in actual_task_args)
