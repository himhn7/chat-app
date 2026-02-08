# Architecture Diagram

```mermaid
flowchart LR
    U[User Browser]
    FE[React Frontend<br/>Axios + react-markdown]
    API[FastAPI Main API<br/>/api/chat]
    EX[FastAPI Extractor Service<br/>/extract]
    LLM[(OpenAI or Anthropic API)]

    U --> FE
    FE -->|prompt + optional file| API
    API -->|multipart file| EX
    EX -->|extracted content| API
    API -->|constructed prompt| LLM
    LLM -->|token stream| API
    API -->|streamed text response| FE
```

## Brief Notes

- The frontend sends prompt and optional file in one request.
- The main API calls an internal extraction microservice before invoking the LLM.
- The final LLM response is streamed back to the frontend for progressive rendering.

