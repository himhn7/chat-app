import asyncio
from typing import AsyncGenerator

from fastapi import HTTPException

from .config import Settings


async def stream_chat(
    *,
    prompt: str,
    temperature: float,
    settings: Settings,
) -> AsyncGenerator[str, None]:
    if settings.mock_llm:
        async for chunk in _stream_mock(prompt):
            yield chunk
        return

    async for chunk in _stream_xai(prompt, temperature, settings):
        yield chunk


async def _stream_mock(prompt: str) -> AsyncGenerator[str, None]:
    snippet = prompt.strip().replace("\n", " ")[:220]
    mock_text = (
        "Mock response (set MOCK_LLM=false and configure API keys for real model output).\n\n"
        f"Prompt preview: {snippet}"
    )
    for token in mock_text.split(" "):
        yield token + " "
        await asyncio.sleep(0.01)


async def _stream_xai(
    prompt: str, temperature: float, settings: Settings
) -> AsyncGenerator[str, None]:
    if not settings.xai_api_key:
        raise HTTPException(status_code=500, detail="Missing XAI_API_KEY")

    try:
        from openai import AsyncOpenAI
    except ImportError as exc:
        raise HTTPException(
            status_code=500,
            detail="OpenAI-compatible SDK not installed. Install from requirements.",
        ) from exc

    client = AsyncOpenAI(api_key=settings.xai_api_key, base_url=settings.xai_base_url)
    stream = await client.chat.completions.create(
        model=settings.xai_model,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
        stream=True,
    )

    async for chunk in stream:
        choices = getattr(chunk, "choices", [])
        if not choices:
            continue
        delta = getattr(choices[0], "delta", None)
        if not delta:
            continue
        text = getattr(delta, "content", None)
        if text:
            yield text
