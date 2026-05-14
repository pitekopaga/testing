# Colorblind API Mock Project
# Software Testing Portfolio 
[![CI](https://github.com/pitekopaga/testing/actions/workflows/ci.yml/badge.svg)](https://github.com/pitekopaga/testing/actions/workflows/ci.yml)

A simple API that determines whether two hex color codes are distinguishable for someone with red-green colorblindness.

## Prerequisites

- Docker installed on your machine
- Git (to clone the repository)
- curl (for testing, or use a REST client like Postman)

## Getting Started

Clone the repository and navigate to the mock-project folder:

```bash
git clone https://github.com/pitekopaga/testing.git
cd testing/mock-project
```

## Step 1: Start the API

```bash
docker compose up --build -d
```

The API will run in the background. You do not need to keep a terminal open.

## Step 2: Test the API manually

Run the following commands one at a time.

### Health check

```bash
curl http://localhost:5000/health
```

Expected output: `{"status":"ok"}`

### Red vs Green (should return false)

```bash
curl -X POST http://localhost:5000/check -H "Content-Type: application/json" -d '{"color1": "#FF0000", "color2": "#00FF00"}'
```

Expected output: `{"distinguishable":false}`

### Red vs Blue (should return true)

```bash
curl -X POST http://localhost:5000/check -H "Content-Type: application/json" -d '{"color1": "#FF0000", "color2": "#0000FF"}'
```

Expected output: `{"distinguishable":true}`

### Missing parameters (should return error)

```bash
curl -X POST http://localhost:5000/check -H "Content-Type: application/json" -d '{"color1": "#FF0000"}'
```

Expected output: `{"error":"Missing color parameters"}` with HTTP 400 status.

## Step 3: Run automated tests

Unit tests:

```bash
docker compose exec api pytest tests/ -v
```

Integration tests:

```bash
docker compose exec api pytest integration_tests/ -v
```

## Step 4: Stop the API

```bash
docker compose down
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Homepage with instructions |
| GET | `/health` | Health check |
| POST | `/check` | Takes `color1` and `color2` as hex codes, returns `distinguishable` (true/false) |

## Troubleshooting

If `curl` is not found, install it with `sudo apt install curl` (Ubuntu) or use a REST client like Postman. If the API does not start, make sure port 5000 is not already in use.
