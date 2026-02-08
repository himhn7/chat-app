from typing import Any

import httpx
from fastapi import HTTPException, UploadFile

from .config import Settings


async def extract_uploaded_file(file: UploadFile, settings: Settings) -> str:
    content = await file.read()
    if not content:
        return ""

    files = {
        "file": (
            file.filename or "upload.bin",
            content,
            file.content_type or "application/octet-stream",
        )
    }

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(f"{settings.extractor_url}/extract", files=files)
    except httpx.HTTPError as exc:
        raise HTTPException(
            status_code=502, detail=f"Extractor service unreachable: {exc}"
        ) from exc

    if response.status_code != 200:
        detail = "Extractor service failed."
        try:
            payload: Any = response.json()
            detail = payload.get("detail", detail)
        except Exception:
            pass
        raise HTTPException(status_code=400, detail=detail)

    payload = response.json()
    extracted_text = payload.get("content", "")
    return extracted_text[: settings.max_context_chars]

