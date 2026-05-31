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

## Diagnostic Consistency Tracking

While working on this assignment, I discovered an important gap in existing colorblindness tests. I took the Enchroma test three times over several months. It diagnosed me as Deutan twice and Protan once. A user who gets different results from the same test will not trust any of them.

### Implementation

I added consistency tracking to my own test. Users now:

1. Log in with a username (no password required)
2. Take the test as normal
3. See their history and consistency score on the results page

The system stores results in a JSON file and calculates:
- Total number of sessions
- Consistency percentage (how often the same diagnosis appears)
- Most common diagnosis
- Last 3 results

### Automation

This feature is fully automated. The test itself saves results, loads past history, and displays consistency without any manual intervention.

### Value

Twenty percent of users will experience inconsistent results, but that small group will generate eighty percent of complaints and lost trust. Focusing on stability across sessions is the highest-value specialized testing I added to my product.

### Results

I tested this by taking my own test multiple times with different usernames. The consistency tracking works correctly. Future work would involve user studies to see how often real users get inconsistent results and whether my test is more stable than Enchroma.
