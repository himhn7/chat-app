# Architecture

This project is a local-first full-stack chat application with optional file context and streamed model output.
For styled/visual presentation, use `ARCHITECTURE_VISUAL.html`.

## System Topology

- User interacts with React frontend.
- Frontend sends prompt and optional file to Main API (`POST /api/chat`).
- Main API sends PDF/Text files to Extractor Service (`POST /extract`).
- Main API calls xAI for chat completion (text or multimodal image).
- Main API streams response chunks back to frontend.
- Frontend renders output progressively.

## End-to-End Request Flow

1. Browser sends `POST /api/chat` with `prompt`, `temperature`, and optional `file`.
2. If file is PDF/Text:
- Main API forwards file to Extractor Service.
- Extractor returns extracted content.
- Main API builds prompt with extracted context.
3. If file is Image:
- Main API reads image bytes.
- Main API calls xAI with multimodal payload (`text + image_url`).
4. If no file:
- Main API calls xAI with prompt-only payload.
5. xAI returns streamed chunks.
6. Main API sends chunked plain-text response to frontend.
7. Frontend updates assistant message while chunks arrive.

## Components and Responsibilities

1. Frontend (`frontend/`)
- Collects prompt/file/temperature.
- Sends one multipart request via Axios.
- Renders streamed markdown output.

2. Main API (`backend/app/main.py`)
- Validates request input.
- Routes PDF/Text files to extractor service.
- Routes image files to xAI multimodal path.
- Streams model output to frontend.

3. Extractor Service (`backend/extractor_service/main.py`)
- Extracts text/metadata from PDF/text/image uploads.
- Used primarily for text-context pipeline.

4. LLM Client Layer (`backend/app/llm_clients.py`)
- Wraps xAI API calls and chunk streaming.
- Supports `MOCK_LLM=true` for no-key local testing.

## Design Decisions

1. Why xAI (Grok) instead of OpenAI/Anthropic
- xAI was selected because a Grok API key was already available.
- This keeps operating cost-efficient while preserving the same integration model (OpenAI-compatible streaming chat completion).

2. Why images are not extractor-first
- For image questions, visual fidelity matters more than metadata/OCR text.
- The app sends the actual image (`text + image_url`) directly to the multimodal model.
- PDF/Text files still use extractor-first flow.

3. Why no database yet
- Current scope is intentionally stateless to reduce setup friction.
- Persistence can be added later without changing the core request pipeline.

## Operational Notes

1. Required backend env
- `XAI_API_KEY`

2. Optional backend env
- `XAI_BASE_URL` (default `https://api.x.ai/v1`)
- `XAI_MODEL` (default `grok-4-1-fast-non-reasoning`)
- `MOCK_LLM=true` for local no-key testing

3. Service ports
- Frontend: `5173`
- Main API: `8000`
- Extractor: `8001`
