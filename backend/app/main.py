from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse

from .config import get_settings
from .extractor_client import extract_uploaded_file
from .llm_clients import stream_chat

app = FastAPI(title="AI Chat API", version="1.0.0")
settings = get_settings()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin] if settings.frontend_origin != "*" else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
async def health() -> JSONResponse:
    return JSONResponse({"status": "ok"})


@app.get("/api/providers")
async def providers() -> JSONResponse:
    settings = get_settings()
    return JSONResponse(
        {
            "provider": "xai",
            "model": settings.xai_model,
        }
    )


def build_prompt(user_prompt: str, file_context: str) -> str:
    prompt_text = user_prompt.strip() or "Please summarize the uploaded file."
    if not file_context:
        return prompt_text
    return (
        "Use the file context below to answer the user request.\n\n"
        f"{file_context}\n"
        "User prompt:\n"
        f"{prompt_text}"
    )


def _is_image_upload(file: UploadFile) -> bool:
    content_type = (file.content_type or "").lower()
    lower_name = (file.filename or "").lower()
    if content_type.startswith("image/"):
        return True
    return lower_name.endswith((".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp"))


@app.post("/api/chat")
async def chat(
    prompt: str = Form(default=""),
    temperature: float = Form(default=0.2),
    file: UploadFile | None = File(default=None),
) -> StreamingResponse:
    if not prompt.strip() and file is None:
        raise HTTPException(status_code=400, detail="Prompt or file is required.")

    settings = get_settings()

    file_context = ""
    image_bytes: bytes | None = None
    image_mime_type: str | None = None

    if file is not None:
        if _is_image_upload(file):
            image_bytes = await file.read()
            image_mime_type = file.content_type or "image/jpeg"
            if not image_bytes:
                raise HTTPException(status_code=400, detail="Uploaded file is empty.")
        else:
            extracted_text = await extract_uploaded_file(file, settings)
            if extracted_text.strip():
                file_context = f"File '{file.filename}' content:\n{extracted_text}\n"

    full_prompt = build_prompt(prompt, file_context)

    async def stream_response():
        async for chunk in stream_chat(
            prompt=full_prompt,
            temperature=temperature,
            settings=settings,
            image_bytes=image_bytes,
            image_mime_type=image_mime_type,
        ):
            yield chunk

    return StreamingResponse(stream_response(), media_type="text/plain")
