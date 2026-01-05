# Development Tickets: Beat Starter SaaS API

Based on `docs/API_SPEC_FINAL.md`.

## 🗄️ Database/Backend (Infrastructure)

| Ticket ID | Title | Description | Acceptance Criteria |
| :--- | :--- | :--- | :--- |
| **DEV-001** | **Setup FastAPI Project Skeleton** | Initialize the `app/` directory with `main.py`, `requirements.txt`, and basic logging config. | Done when `uvicorn app.main:app` runs and returns 404 for `/`. |
| **DEV-002** | **Dockerize Application** | Create a multi-stage `Dockerfile` optimized for Python 3.10+ production size. | Done when `docker run -p 8000:8000 beat-api` starts the server successfully. |
| **DEV-003** | **Migrate Core Logic to Service** | Refactor `src/generator.py` and utils into an injectable service class `BeatService`. | Done when `BeatService.generate(...)` can be imported and run from `app/main.py`. |

## 🔌 API/Logic

| Ticket ID | Title | Description | Acceptance Criteria |
| :--- | :--- | :--- | :--- |
| **DEV-004** | **Define Pydantic Models** | Create `GenerationRequest` and `GenerationResponse` classes matching the JSON schema. | Done when invalid JSON input triggers a standard Pydantic validation error (422). |
| **DEV-005** | **Implement POST /v1/generate** | Connect the endpoint to `BeatService` and return Base64 MIDI data. | Done when a POST request returns a valid JSON with `midi_base64` string. |
| **DEV-006** | **Implement GET /health** | Add a lightweight liveness probe endpoint. | Done when `curl /health` returns `{"status": "ok"}` with 200 OK. |
| **DEV-007** | **Add Error Handling Middleware** | Implement a global exception handler for 400 (Bad Logic) and 500 (Crash) errors. | Done when a simulated crash returns a clean JSON error `{ "detail": "..." }` instead of an HTML stack trace. |

## 🎨 Frontend/UI (Out of Scope for API Phase)

*Skipped per Spec Scope (API Service only)*

## 🧪 Testing

| Ticket ID | Title | Description | Acceptance Criteria |
| :--- | :--- | :--- | :--- |
| **DEV-008** | **Unit Tests for Service Layer** | Write tests for `BeatService` ensuring it handles all parameters (keys, scales). | Done when `pytest` passes with >90% coverage on the service logic. |
| **DEV-009** | **Integration Tests for Endpoints** | Write `TestClient` tests for `/v1/generate` (Success, Invalid Input). | Done when tests confirm 200 OK for valid data and 422 for bad data. |
| **DEV-010** | **Load Test (Performance)** | Verify the "under 200ms" requirement using `locust` or a script. | Done when 50 concurrent users average <200ms response time. |
