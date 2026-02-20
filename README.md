# Real-Time Analytics Backend API

## Project Overview

This project is a **production-grade backend API** for a simulated real-time analytics service.

It demonstrates how to build **high-performance, fault-tolerant backend systems** using modern resilience patterns such as **Redis caching, rate limiting, and circuit breakers**, all deployed using **Docker**.

The application is designed to handle:
- High request volumes
- Repeated read operations efficiently
- External service failures gracefully

---

## Key Features

- RESTful API built with FastAPI
- Redis-backed read-through caching
- Redis-backed rate limiting
- Circuit breaker pattern for external service protection
- Fully Dockerized using Docker & Docker Compose
- Automated unit and integration tests

---

## Tech Stack

- **Backend Framework:** FastAPI (Python)
- **Caching & Rate Limiting:** Redis
- **Containerization:** Docker, Docker Compose
- **Testing:** Pytest
- **Runtime:** Python 3.9+

---

## Architecture Overview

- Metrics are ingested via REST APIs
- Aggregated metric summaries are cached in Redis
- Rate limiting prevents API abuse
- Circuit breaker protects calls to an unreliable external service
- Application and Redis run in isolated Docker containers

---

## Project Structure

```

.
├── src/
│   ├── main.py                 # Application entry point
│   ├── api/
│   │   └── metrics.py          # API endpoints
│   ├── services/
│   │   ├── cache_service.py    # Redis caching logic
│   │   ├── rate_limiter.py     # Redis rate limiting
│   │   ├── circuit_breaker.py  # Circuit breaker implementation
│   │   └── external_service.py # External service simulator
│   └── config/
│       └── settings.py         # Environment & config loading
├── tests/
│   ├── test_api_integration.py # API + Redis integration tests
│   ├── test_rate_limiting.py   # Rate limiter tests
│   └── test_circuit_breaker.py # Circuit breaker tests
├── Dockerfile                  # Backend container definition
├── docker-compose.yml          # App + Redis orchestration
├── requirements.txt            # Python dependencies
├── .env.example                # Environment variables reference
└── README.md                   # Project documentation

````

---

## Prerequisites

Ensure the following are installed:

- Docker
- Docker Compose
- Git

---

## Setup Instructions (For Testers)

### 1. Clone the Repository

```bash
git clone https://github.com/gollapallijayanthi/realtime-analytics-backend.git
cd realtime-analytics-backend
````

---

### 2. Build and Run the Application

```bash
docker-compose up --build
```

This will:

* Build the backend image
* Start Redis
* Start the FastAPI application
* Wait for health checks to pass

---

### 3. Verify Application Health

```bash
curl http://localhost:8000/health
```

Expected response:

```json
{"status":"ok"}
```

---

## API Testing Guide

### 1. Create a Metric

**POST /api/metrics**

```bash
curl -X POST http://localhost:8000/api/metrics \
-H "Content-Type: application/json" \
-d '{"timestamp":"2025-01-01T10:00:00","value":75,"type":"cpu"}'
```

Expected response:

```json
{"message":"Metric stored successfully"}
```

---

### 2. Get Metric Summary (Cached)

**GET /api/metrics/summary**

```bash
curl "http://localhost:8000/api/metrics/summary?metric_type=cpu"
```

Expected response:

```json
{"type":"cpu","count":1,"average":75.0}
```

✔ This endpoint uses **Redis read-through caching**
✔ Repeated calls are served from cache while TTL is valid

---

### 3. Verify Redis Cache

```bash
docker exec -it realtime-analytics-backend-redis-1 redis-cli
KEYS *
```

Expected output example:

```
1) "summary:cpu"
```

---

## Rate Limiting Verification

Rate limit is enforced on **POST /api/metrics**

* Default limit: **5 requests per minute per IP**

```bash
for i in {1..6}; do
  curl -X POST http://localhost:8000/api/metrics \
  -H "Content-Type: application/json" \
  -d '{"timestamp":"2025-01-01T10:00:00","value":50,"type":"cpu"}'
done
```

Expected behavior:

* First 5 requests → success
* 6th request → rejected

Expected response:

```json
{"detail":"Too many requests"}
```

HTTP status:

```
429 Too Many Requests
```

Includes `Retry-After` header.

---

## Circuit Breaker Verification

### External Service Endpoint

**GET /external**

```bash
curl http://localhost:8000/external
```

Normal response:

```json
{"external":"ok","value":134}
```

When failure threshold is exceeded, circuit opens and fallback is returned:

```json
{"fallback":true,"reason":"external service failure"}
```

✔ Circuit transitions through:

* Closed
* Open
* Half-Open
* Closed (on recovery)

---

## Running Automated Tests

All unit and integration tests can be executed locally using:

```bash
pytest
```

Expected output:

```
==================== test session starts ====================
collected 5 items

tests/test_api_integration.py ...
tests/test_circuit_breaker.py .
tests/test_rate_limiting.py .

==================== 5 passed in Xs ====================
```

✔ Tests cover:

* API behavior
* Redis caching
* Rate limiting
* Circuit breaker state transitions

---

## Docker & Health Checks

* Application and Redis run in separate containers
* Redis health check included
* Application health check validates `/health`
* `depends_on` ensures correct startup order

---

## Environment Configuration

All configuration values are externalized via environment variables.

See `.env.example` for reference.

---

## Conclusion

This project demonstrates a **fault-tolerant, scalable backend API** using modern distributed systems patterns.
It is production-ready and suitable for real-world backend engineering roles.


