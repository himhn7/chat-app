import pytest
from httpx import ASGITransport, AsyncClient

from extractor_service.main import app


@pytest.mark.asyncio
async def test_extract_plain_text() -> None:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post(
            "/extract",
            files={"file": ("note.txt", b"hello extractor", "text/plain")},
        )

    assert response.status_code == 200
    payload = response.json()
    assert payload["content"] == "hello extractor"


@pytest.mark.asyncio
async def test_extract_unsupported_file() -> None:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post(
            "/extract",
            files={"file": ("archive.zip", b"PK123", "application/zip")},
        )

    assert response.status_code == 400
    assert "Unsupported file type" in response.json()["detail"]

