# Spec Audit Report

## Score: 4/10

## Critical Issues
*   **Vague Metrics**: "The API must be fast" is not testable. Needs a specific latency target (e.g., <500ms).
*   **Missing Schema**: The `Input` JSON for `/generate` is not defined. Developers don't know what fields to send.
*   **Undefined Errors**: "Return an error" is insufficient. Needs specific HTTP Status Codes (400 vs 500) and an error response body format.
*   **Response Format**: "The MIDI file" is ambiguous. Is it a binary download? A Base64 string? A link to S3?

## Visual Gaps
*   **Flowchart**: A diagram showing the Request -> Validation -> Generator -> MIDI Writer -> Response flow is needed to clarify the pipeline.

## Refined Snippets

### Refined 4.1 Generate Beat
*   **URL**: `/v1/generate`
*   **Method**: `POST`
*   **Content-Type**: `application/json`
*   **Request Body**:
    ```json
    {
      "key": "C" (string, default="C"),
      "scale": "minor" (enum: ["minor", "major", "phrygian"], default="minor"),
      "tempo": 140 (int, range: 60-200),
      "options": {
        "chords": true (bool),
        "drums": true (bool)
      }
    }
    ```
*   **Success Response (200 OK)**:
    *   **Content-Type**: `application/json`
    *   **Body**:
        ```json
        {
          "status": "success",
          "data": {
            "midi_base64": "<base64_string>",
            "metadata": { "duration_sec": 12.5 }
          }
        }
        ```
*   **Error Response (400 Bad Request)**:
    *   **Body**: `{ "error": "Invalid tempo. Must be between 60 and 200." }`
