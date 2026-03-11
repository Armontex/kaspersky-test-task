import pytest
from unittest.mock import MagicMock, AsyncMock
from httpx import AsyncClient
from src.fastapi_app import app
from src.services.analyzer.api.routers.export_report import (
    get_analyze_file_task,
    get_write_file,
)


async def test_export_report_success(async_client: AsyncClient):
    mock_task = MagicMock()
    mock_write = AsyncMock()

    app.dependency_overrides[get_analyze_file_task] = lambda: mock_task
    app.dependency_overrides[get_write_file] = lambda: mock_write

    file_data = {"file": ("test.txt", b"hello world", "text/plain")}

    response = await async_client.post("public/report/export", files=file_data)

    assert response.status_code == 202

    mock_write.assert_called_once()

    mock_task.delay.assert_called_once()

    args, _ = mock_task.delay.call_args
    assert isinstance(args[0], str)
    assert isinstance(args[1], str)
