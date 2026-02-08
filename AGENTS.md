# AGENTS

## Project Goals

1. Provide a web chat UI for ChatGPT or Claude.
2. Accept user prompt plus optional uploaded file (PDF, text, image).
3. Extract file context through a dedicated Python microservice.
4. Build a combined prompt and stream LLM output back to the UI.
5. Keep setup and testing simple for local development.

## Project Structure

```text
.
|- backend/
|  |- app/
|  |  |- config.py              # dotenv-backed settings
|  |  |- extractor_client.py    # calls extractor microservice
|  |  |- llm_clients.py         # OpenAI/Anthropic streaming logic
|  |  `- main.py                # primary FastAPI app
|  |- extractor_service/
|  |  `- main.py                # PDF/text/image content extraction API
|  |- tests/
|  |  |- test_api.py
|  |  `- test_extractor.py
|  |- requirements.txt
|  `- .env.example
|- frontend/
|  |- src/
|  |  |- components/FileUpload.jsx
|  |  |- App.jsx
|  |  |- main.jsx
|  |  `- styles.css
|  |- index.html
|  |- package.json
|  `- vite.config.js
|- scripts/
|  |- setup_backend.ps1
|  |- run_api.ps1
|  |- run_extractor.ps1
|  |- test_backend.ps1
|  `- test_frontend.ps1
|- ARCHITECTURE.md
`- README.md
```

## Runtime Flow

1. Frontend posts prompt + optional file to `POST /api/chat`.
2. Main API forwards uploaded file to extractor microservice.
3. Extractor returns text/metadata from the file.
4. Main API constructs final prompt and calls selected LLM provider.
5. Main API streams output tokens back to frontend.

