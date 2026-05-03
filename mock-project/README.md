# Colorblind API Mock Project

## Start the API

```bash
docker compose up --build -d
```

## Test the API manually

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

## Run automated tests

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
