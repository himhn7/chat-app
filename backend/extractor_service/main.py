from io import BytesIO

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from PIL import Image
from PyPDF2 import PdfReader

from app.config import get_settings

app = FastAPI(title="Extractor Service", version="1.0.0")


def _extract_text(content: bytes) -> str:
    for encoding in ("utf-8", "latin-1"):
        try:
            return content.decode(encoding)
        except UnicodeDecodeError:
            continue
    return ""


def _extract_pdf(content: bytes) -> str:
    reader = PdfReader(BytesIO(content))
    text_parts: list[str] = []
    for page in reader.pages:
        text_parts.append(page.extract_text() or "")
    return "\n".join(text_parts).strip()


def _extract_image(content: bytes) -> str:
    image = Image.open(BytesIO(content))
    details = (
        f"Image metadata: format={image.format}, mode={image.mode}, size={image.width}x{image.height}."
    )

    try:
        import pytesseract  # Optional OCR dependency.

        ocr_text = pytesseract.image_to_string(image).strip()
    except Exception:
        ocr_text = ""

    if ocr_text:
        return f"{details}\nOCR text:\n{ocr_text}"
    return details


@app.get("/health")
async def health() -> JSONResponse:
    return JSONResponse({"status": "ok"})


@app.post("/extract")
async def extract(file: UploadFile = File(...)) -> JSONResponse:
    settings = get_settings()
    filename = file.filename or "uploaded_file"
    content_type = (file.content_type or "").lower()
    content = await file.read()

    if not content:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    lower_name = filename.lower()
    extracted = ""

    if content_type == "application/pdf" or lower_name.endswith(".pdf"):
        extracted = _extract_pdf(content)
    elif content_type.startswith("text/") or lower_name.endswith(
        (".txt", ".md", ".csv", ".json", ".log")
    ):
        extracted = _extract_text(content)
    elif content_type.startswith("image/") or lower_name.endswith(
        (".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp")
    ):
        extracted = _extract_image(content)
    else:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type. Upload PDF, text, or image files.",
        )

    extracted = extracted.strip()
    extracted = extracted[: settings.max_extract_chars]

    return JSONResponse(
        {
            "filename": filename,
            "content_type": content_type,
            "content": extracted,
        }
    )

