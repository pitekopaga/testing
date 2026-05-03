# Colorblind API Mock Project

A demonstration web API that checks whether two hex colors are distinguishable for someone with red-green colorblindness. This is a simplified demo with limited functionality.

## Prerequisites

- Docker installed on your machine
- Git (to clone the repository)

## Getting Started

Clone the repository and navigate to the mock-project folder:

```bash
git clone https://github.com/pitekopaga/testing.git
cd testing/mock-project
```

## Run the API

```bash
docker compose up --build -d
```

The API will run in the background.

## Open the Web Interface

Open your browser and go to: `http://localhost:5000`

You will see a web page where you can enter two hex colors and click "Check". The page will tell you whether the colors are distinguishable according to this simplified demo.

## Test the API manually with curl (optional)

Health check:

```bash
curl http://localhost:5000/health
```

Expected output: `{"status":"ok"}`

Red vs Green (should return false):

```bash
curl -X POST http://localhost:5000/check -H "Content-Type: application/json" -d '{"color1": "#FF0000", "color2": "#00FF00"}'
```

Expected output: `{"distinguishable":false}`

Red vs Blue (should return true):

```bash
curl -X POST http://localhost:5000/check -H "Content-Type: application/json" -d '{"color1": "#FF0000", "color2": "#0000FF"}'
```

Expected output: `{"distinguishable":true}`

Missing parameters (should return error):

```bash
curl -X POST http://localhost:5000/check -H "Content-Type": application/json" -d '{"color1": "#FF0000"}'
```

Expected output: `{"error":"Missing color parameters"}` with HTTP 400 status.

## Run Automated Tests

Unit tests:

```bash
docker compose exec api pytest tests/ -v
```

Integration tests:

```bash
docker compose exec api pytest integration_tests/ -v
```

## Stop the API

```bash
docker compose down
```

## Limitations

This is a simplified demonstration. The current version only knows that pure red (#FF0000) and pure green (#00FF00) are indistinguishable, and that pure red and pure blue (#0000FF) are distinguishable. For all other color pairs, it assumes they are distinguishable. A real implementation would use perceptual distance algorithms.
