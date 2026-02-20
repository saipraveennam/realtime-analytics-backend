# Realtime Analytics Backend
---

# 🚀 Realtime Analytics Backend

## 📌 Overview

This project is a scalable and production-ready backend API designed to simulate a real-time analytics system.

It showcases how to design high-performance and resilient backend services using modern engineering practices such as:

* Redis-based caching
* API rate limiting
* Circuit breaker pattern
* Docker-based containerization

The system is built to efficiently handle high traffic, optimize repeated read operations, and gracefully manage external service failures.

---

## ✨ Core Features

* REST API built with **FastAPI**
* Read-through caching using **Redis**
* API rate limiting (per IP basis)
* Circuit breaker implementation for external dependency handling
* Fully containerized using **Docker & Docker Compose**
* Automated unit and integration testing

---

## 🛠 Tech Stack

* **Backend Framework:** FastAPI (Python)
* **Caching & Rate Limiting:** Redis
* **Containerization:** Docker & Docker Compose
* **Testing:** Pytest
* **Python Version:** 3.9+

---

## 🏗 System Architecture

* Metrics are submitted through REST endpoints
* Metric summaries are computed and cached in Redis
* Rate limiter restricts excessive API usage
* Circuit breaker protects unstable external service calls
* Backend and Redis run as separate Docker containers

---

## 📁 Project Structure

```
.
├── src/
│   ├── main.py
│   ├── api/
│   │   └── metrics.py
│   ├── services/
│   │   ├── cache_service.py
│   │   ├── rate_limiter.py
│   │   ├── circuit_breaker.py
│   │   └── external_service.py
│   └── config/
│       └── settings.py
├── tests/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── README.md
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/saipraveennam/Realtime-analytics-backend.git
cd Realtime-analytics-backend
```

---

### 2️⃣ Build & Run with Docker

```bash
docker-compose up --build
```

This will:

* Build backend container
* Start Redis container
* Launch FastAPI application

---

### 3️⃣ Health Check

```bash
curl http://localhost:8000/health
```

Expected response:

```json
{"status":"ok"}
```

---

## 📊 API Usage

### ➤ Create Metric

**POST** `/api/metrics`

```bash
curl -X POST http://localhost:8000/api/metrics \
-H "Content-Type: application/json" \
-d '{"timestamp":"2025-01-01T10:00:00","value":75,"type":"cpu"}'
```

Response:

```json
{"message":"Metric stored successfully"}
```

---

### ➤ Get Metric Summary (Cached)

**GET** `/api/metrics/summary`

```bash
curl "http://localhost:8000/api/metrics/summary?metric_type=cpu"
```

Response:

```json
{"type":"cpu","count":1,"average":75.0}
```

✔ Uses Redis caching
✔ Repeated calls served from cache (based on TTL)

---

## 🚦 Rate Limiting

* Limit: 5 requests per minute per IP
* Applied on: `POST /api/metrics`
* Exceeded limit returns:

```json
{"detail":"Too many requests"}
```

HTTP Status: `429 Too Many Requests`

---

## 🔌 Circuit Breaker

Endpoint: `/external`

Normal response:

```json
{"external":"ok","value":134}
```

If failure threshold exceeds:

```json
{"fallback":true,"reason":"external service failure"}
```

Circuit States:

* Closed
* Open
* Half-Open
* Closed (after recovery)

---

## 🧪 Running Tests

```bash
pytest
```

Tests validate:

* API functionality
* Redis caching
* Rate limiting logic
* Circuit breaker behavior

---

## 🐳 Docker Configuration

* Separate containers for backend & Redis
* Health checks enabled
* Proper service dependency management using `depends_on`

---

## 🔧 Environment Variables

All configuration values are environment-based.

Refer `.env.example` file for available variables.

---

## 📈 Final Note

This project demonstrates backend system design with scalability, resilience, and production-readiness in mind. It reflects modern backend engineering best practices.

---


