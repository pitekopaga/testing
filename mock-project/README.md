# Colorblind API Mock Project

A simple API that determines whether two hex color codes are distinguishable for someone with red-green colorblindness.

## Prerequisites

- Docker installed on your machine
- Git (to clone the repository)

## Getting Started

Clone the repository and navigate to the mock-project folder:

```bash
git clone https://github.com/pitekopaga/testing.git
cd testing/mock-project
```

## Running the API

Start the API server:

```bash
docker compose up --build -d
```

The API will be available at `http://localhost:5000`.

## Testing the API manually

Health check:

```bash
curl http://localhost:5000/health
```

Red vs Green (should return false):

```bash
curl -X POST http://localhost:5000/check -H "Content-Type: application/json" -d '{"color1": "#FF0000", "color2": "#00FF00"}'
```

Red vs Blue (should return true):

```bash
curl -X POST http://localhost:5000/check -H "Content-Type: application/json" -d '{"color1": "#FF0000", "color2": "#0000FF"}'
```

Missing parameters (should return error):

```bash
curl -X POST http://localhost:5000/check -H "Content-Type: application/json" -d '{"color1": "#FF0000"}'
```

## Running Automated Tests

Unit tests:

```bash
docker compose exec api pytest tests/ -v
```

Integration tests:

```bash
docker compose exec api pytest integration_tests/ -v
```

## Stopping the API

```bash
docker compose down
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| POST | `/check` | Takes `color1` and `color2` as hex codes, returns `distinguishable` (true/false) |
