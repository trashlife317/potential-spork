# Technical Specification: Beat Starter API Service (DRAFT)

## 1. Introduction
We are building a REST API service for the Beat Starter engine. This will allow web and mobile applications to request generated MIDI files.

## 2. Goals
*   Expose the current Python generation logic via HTTP.
*   Make it deployable to the cloud.
*   Ensure it handles errors well.

## 3. System Architecture
*   **Language**: Python 3.10+
*   **Framework**: FastAPI
*   **Server**: Uvicorn/Gunicorn
*   **Container**: Docker

## 4. API Endpoints

### 4.1 Generate Beat
*   **URL**: `/generate`
*   **Method**: POST
*   **Input**: JSON object with key, scale, tempo, etc.
*   **Output**: The MIDI file.

### 4.2 Health Check
*   **URL**: `/health`
*   **Method**: GET
*   **Output**: "OK"

## 5. Requirements
*   The API must be fast.
*   The API must return a standard MIDI file.
*   If the user sends bad data, return an error.
