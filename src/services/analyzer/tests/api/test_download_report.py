from unittest.mock import MagicMock
from src.fastapi_app import app
from src.services.analyzer.api.routers.download_report import (
    get_is_path_exists,
    get_build_file_response,
)


async def test_download_report_success_di(async_client):

    app.dependency_overrides[get_is_path_exists] = lambda: lambda path: True
    mock_response = MagicMock()
    app.dependency_overrides[get_build_file_response] = (
        lambda: lambda path: mock_response
    )

    response = await async_client.get("public/report/download/some_uuid")

    assert response.status_code == 200.0


async def test_download_report_not_found_di(async_client):
    app.dependency_overrides[get_is_path_exists] = lambda: lambda path: False

    response = await async_client.get("public/report/download/missing_id")

    assert response.status_code == 404
    assert response.json()["detail"] == "Файл не найден или еще не готов"
