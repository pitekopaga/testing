# Test Strategy - Color Vision Diagnostic Test

## Area Under Test

A web-based Ishihara-style color vision test that diagnoses Protan, Deutan, and Tritan color blindness. The application includes user login, persistent result history, consistency scoring, CSV export, and an optional survey for accuracy feedback.

## Test Approach

- **Unit Testing**: Pattern generation logic and scoring algorithm (pytest)
- **Integration Testing**: API health endpoint and form submission flow (pytest)
- **E2E Testing**: Full user flow including login, test completion, results display, and logout (Playwright)
- **Load Testing**: Concurrent user simulation (Locust)
- **Manual Testing**: Cross-browser validation, accessibility, and diagnostic accuracy verification

## Tools

- pytest for unit and integration tests
- Playwright for E2E browser tests
- Locust for load testing
- Docker for environment isolation
- GitHub Actions for CI/CD

## Quality Metrics

- Unit test pass rate
- E2E test pass rate
- Load test success rate
- User consistency score (across multiple sessions)
- Survey feedback on diagnostic accuracy

## Test Environment

- Docker container with Python 3.11
- Browser: Chromium (headless for CI, headed for manual)
- CI: GitHub Actions (Ubuntu latest)
