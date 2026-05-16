# Golden Paths Analysis

## What users pay for

Users pay for an accurate color blindness diagnosis. The most valuable scenario is a user completing the full test and receiving a reliable result that matches clinical tests.

## Golden Path 1: Complete diagnostic test

A user opens the web application, answers all test plates by typing the numbers they see (or 0 if they see nothing), and receives a diagnosis with cone percentage scores.

**Why this is valuable:** This is the core value proposition. Without an accurate diagnosis, the test has no value.

## Golden Path 2: Retaking the test

A user completes the test, receives a result, and clicks "Take Test Again" to start a fresh session with randomized plates.

**Why this is valuable:** Users may want to verify their results or test again after the variance disclaimer. This also demonstrates that the test is not deterministic.

## Golden Path 3: Health check for operations

A DevOps engineer calls the `/health` endpoint to verify the service is running before routing traffic.

**Why this is valuable:** For enterprise deployment, reliability monitoring is essential. Users cannot take the test if the service is down.

## E2E tests covering these paths

| Golden Path | E2E Test |
|-------------|----------|
| Complete diagnostic test | `user can submit answers and complete the test` |
| Retaking the test | `reset button clears results and restarts test` |
| Health check | `health endpoint returns ok` |
