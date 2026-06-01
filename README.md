# Software Testing Portfolio

[![CI](https://github.com/pitekopaga/testing/actions/workflows/ci.yml/badge.svg)](https://github.com/pitekopaga/testing/actions/workflows/ci.yml)

This repository contains my work from CSS 508 at UW Bothell, demonstrating software testing practices including test automation, CI/CD, containerization, and AI-native testing workflows.

## Featured Project: Color Vision Diagnostic Test

A web-based Ishihara-style color vision test that diagnoses Protan (red deficiency), Deutan (green deficiency), and Tritan (blue deficiency) color blindness. The test tracks user history across sessions and provides consistency scoring.

### Features

- User login with persistent result history
- Randomized test plates with "No Number" button
- Cone percentage scores (red, green, blue)
- Consistency tracking across multiple test sessions
- CSV export of all test results with timestamps
- Docker containerization for reproducible environments

### Test Coverage

- **Unit tests**: Scoring algorithm and helper functions (3 tests)
- **Integration tests**: API health endpoint (1 test)
- **E2E tests**: Full user flow with Playwright (5 tests)
- **Load tests**: Locust simulation with 5 concurrent users

### CI/CD Pipeline

GitHub Actions runs all tests automatically on every push:
- Unit and integration tests
- E2E tests with Playwright
- Load tests with Locust

### Technologies

- **Backend**: Python, Flask
- **Frontend**: HTML/CSS, Canvas API
- **Testing**: pytest, Playwright, Locust
- **CI/CD**: GitHub Actions
- **Containerization**: Docker, Docker Compose

## Repository Structure

```
testing/
├── docs/               # Test strategy, plan, reports, and reflections
├── mock-project/       # Color vision diagnostic test application
│   ├── backend/        # Flask API and scoring logic
│   ├── e2e_tests/      # Playwright E2E tests
│   ├── load_tests/     # Locust load test scripts
│   └── unit_tests/     # Pytest unit tests
└── .github/workflows/  # CI/CD pipeline definitions
```

## Running the Project

```bash
cd mock-project
docker compose up --build -d
```

Open your browser to `http://localhost:5000`

## Running Tests

```bash
cd mock-project
docker compose exec api pytest unit_tests/ -v
npx playwright test
locust -f load_tests/locustfile.py --headless -u 5 -r 1 --run-time 30s
```

## License

MIT
