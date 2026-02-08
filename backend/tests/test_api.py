import pytest
from httpx import ASGITransport, AsyncClient

from app.config import reset_settings_cache
from app.main import app


@pytest.mark.asyncio
async def test_health() -> None:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


@pytest.mark.asyncio
async def test_chat_mock_stream(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("MOCK_LLM", "true")
    reset_settings_cache()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/api/chat", data={"prompt": "Say hello from a test."})

    assert response.status_code == 200
    assert "Mock response" in response.text


@pytest.mark.asyncio
async def test_chat_with_uploaded_file(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("MOCK_LLM", "true")
    reset_settings_cache()

    from app import main as main_module

    async def fake_extractor(*args, **kwargs) -> str:
        return "Invoice total is 250 USD."

    monkeypatch.setattr(main_module, "extract_uploaded_file", fake_extractor)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post(
            "/api/chat",
            data={"prompt": "What is the total?"},
            files={"file": ("invoice.txt", b"total=250", "text/plain")},
        )

    assert response.status_code == 200
    assert "Prompt preview:" in response.text
    assert "Invoice total is 250 USD." in response.text
