# Test Plan - Color Vision Diagnostic Test

## Features to Test

1. User login and session management
2. Ishihara plate generation with randomized numbers
3. Answer submission (number input and "No Number" button)
4. Scoring algorithm (red, green, blue cone percentages)
5. Diagnosis determination (Protan, Deutan, Tritan, Normal)
6. Result history and consistency tracking
7. CSV export of all user results
8. Optional survey for accuracy feedback
9. Logout and session cleanup

## Test Cases

### Unit Tests (3 tests)
- `test_result_page_returns_200`: Verifies results page loads
- `test_health_endpoint_returns_ok`: Verifies health endpoint
- `test_debug_stats_endpoint_returns_stats`: Verifies monitoring endpoint

### Integration Tests (1 test)
- `test_health_endpoint`: Verifies `/health` returns 200 OK

### E2E Tests (5 tests)
- Login screen loads
- User can log in and start test
- User can complete all plates and reach results
- Results page shows cone scores
- Exit button logs out and returns to login

### Load Tests (Locust)
- 5 concurrent users submitting answers for 30 seconds
- Monitors response times and error rates

## Setup Steps

```bash
docker compose up --build -d
docker compose exec api pytest unit_tests/ -v
docker compose exec api pytest integration_tests/ -v
npx playwright test
locust -f load_tests/locustfile.py --headless -u 5 -r 1 --run-time 30s
