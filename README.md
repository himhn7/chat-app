# Full-Stack AI Chat App (FastAPI + React + xAI)

This project provides an xAI chat interface with support for:

- Text prompts
- File uploads (`.pdf`, text files, images)
- File content extraction through a dedicated Python microservice
- Streaming responses back to the frontend

See `ARCHITECTURE.md` for a brief architecture diagram.

## Tech Stack

- Frontend: React (Hooks), Axios, react-markdown, Vite
- Backend API: FastAPI, CORS, dotenv
- Extractor microservice: FastAPI + PyPDF2 + Pillow
- LLM SDK: OpenAI-compatible SDK (used for xAI)
- Tests: pytest + httpx (ASGI transport)

## Project Structure

```text
.
|- backend/
|  |- app/
|  |- extractor_service/
|  |- tests/
|  |- requirements.txt
|  `- .env.example
|- frontend/
|  |- src/
|  `- package.json
|- scripts/
|  |- setup_backend.ps1
|  |- run_api.ps1
|  |- run_extractor.ps1
|  |- test_backend.ps1
|  `- test_frontend.ps1
|- ARCHITECTURE.md
|- AGENTS.md
`- README.md
```

## Setup

### 1. Create Python virtual environment

```powershell
py -3 -m venv .venv
.\.venv\Scripts\activate
```

If `py` is unavailable:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

### 2. Install backend dependencies

```powershell
python -m pip install --upgrade pip
python -m pip install -r .\backend\requirements.txt
```

### 3. Configure environment variables

```powershell
Copy-Item .\backend\.env.example .\backend\.env
```

Set:

- `XAI_API_KEY`

For local verification without real keys:

- set `MOCK_LLM=true`

### 4. Install frontend dependencies

```powershell
cd .\frontend
npm install
cd ..
```

## Run

Start everything (extractor + API + frontend) in one step:

```powershell
.\start-dev.cmd
```

Or run services individually:

Run extractor microservice:

```powershell
.\scripts\run_extractor.ps1
```

Run main API server:

```powershell
.\scripts\run_api.ps1
```

Run frontend:

```powershell
cd .\frontend
npm run dev
```

App URLs:

- Frontend: `http://localhost:5173`
- API: `http://localhost:8000`
- Extractor service: `http://localhost:8001`

## Testing

Backend tests:

```powershell
.\scripts\test_backend.ps1 -InstallDeps
```

Frontend smoke test (build):

```powershell
.\scripts\test_frontend.ps1 -InstallDeps
```

## Notes

- Streaming is implemented as chunked plain text from FastAPI to the React UI.
- The frontend uses Axios for API calls and progressive download updates.
- Backend provider is fixed to xAI (no provider/model selector in UI).
