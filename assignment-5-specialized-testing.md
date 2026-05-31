# Specialized Testing Report

## Load Testing (Automated)

I implemented load testing using Locust. The test simulates 10 concurrent users submitting answers over 30 seconds.

### How to run
```bash
cd mock-project
docker compose up --build -d
./run-load-test.sh
```

### Results (local run)
- Health endpoint: 100% success, average response <10ms
- Form submission: 100% success, average response ~150ms
- No crashes or timeouts observed

### Limitation
This is a minimal load test. The Flask development server is single-threaded. A production deployment would need gunicorn or a WSGI server.

## Stress Testing (Not Automated)

I did not automate stress testing. The Flask development server is not designed for high load. This is documented as manual testing.

## Scoring Algorithm Unit Tests (Automated)

I added unit tests for:
- Health endpoint returns 200 OK
- Result page loads without crashing
- Debug stats endpoint returns CPU, memory, and session metrics

All 3 tests pass.

## Operational Monitoring (Implemented)

I added a `/debug/stats` endpoint that returns:
- CPU percentage
- Memory percentage
- Active session count

## SOA/REST Observations

Following Fielding's REST constraints (SRC-3, SRC-27):

- **Statelessness violation**: The current design uses server-side sessions. This creates a scalability bottleneck. A stateless design (client-side storage or JWTs) would be more aligned with REST principles.

- **Service boundaries** (SRC-5): The application has implicit boundaries between the UI, scoring logic, and session store. Documenting these boundaries helps with integration testing.
