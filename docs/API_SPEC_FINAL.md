# Technical Specification: Beat Starter API Service (FINAL)

## 1. Introduction
This document defines the architecture and API contract for the **Beat Starter API**, a microservice that exposes the MIDI composition engine via RESTful endpoints.

## 2. Goals
*   **Access**: Provide a public-facing API for generating multi-track MIDI files (Melody, Chords, Drums).
*   **Scalability**: Containerize the application using Docker for cloud deployment (AWS/GCP).
*   **Performance**: Ensure MIDI generation completes in under 200ms (P95).

## 3. System Architecture
*   **Runtime**: Python 3.10+
*   **Web Framework**: FastAPI (for automatic OpenAPI validation).
*   **Server**: Uvicorn (ASGI) managed by Gunicorn.
*   **Core Logic**: Reuses existing `src.generator`, `src.accompaniment`, and `src.midi_utils` modules.

## 4. API Specification

### 4.1 `POST /v1/generate`
Generates a Beat Starter MIDI file based on provided musical parameters.

**Request:**
*   **Content-Type**: `application/json`
*   **Body Schema**:
    ```json
    {
      "key": "C",             // String. Valid: "A"-"G", sharps as "#". Default: "C"
      "scale": "minor",       // Enum: ["minor", "harmonic_minor", "phrygian", "pentatonic"]. Default: "minor"
      "tempo": 140,           // Integer. Range: 40-240. Default: 140
      "bars": 4,              // Integer. Range: 4-16. Default: 4
      "variation": "B",       // Enum: ["A", "B", "C"]. Default: "B"
      "include_chords": true, // Boolean. Default: true
      "include_drums": true   // Boolean. Default: true
    }
    ```

**Response (200 OK):**
Returns a JSON object containing the binary MIDI data encoded as Base64.
*   **Content-Type**: `application/json`
*   **Body**:
    ```json
    {
      "meta": {
        "key": "C",
        "scale": "minor",
        "tempo": 140
      },
      "midi_base64": "TVRoZAAAAAYAAAABA..." // Base64 encoded .mid file
    }
    ```

**Errors:**
*   **400 Bad Request**: Invalid input (e.g., Tempo = 999).
    *   Body: `{ "detail": "Tempo must be between 40 and 240." }`
*   **500 Internal Server Error**: Unexpected generation failure.

### 4.2 `GET /health`
Liveness probe for load balancers.
*   **Response (200 OK)**: `{"status": "ok", "version": "1.0.0"}`

## 5. Deployment
*   **Docker**: Multi-stage build to minimize image size.
*   **Port**: Expose 8000.
*   **Environment Variables**: `WORKERS` (default 1), `LOG_LEVEL` (default info).
