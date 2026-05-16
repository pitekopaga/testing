# Golden Paths Analysis

## What users pay for

Users pay for accurate colorblindness diagnosis. The most valuable scenario is a user completing the full test and receiving a reliable result.

## Golden Path 1: Quick check via API

A developer integrates the API into their workflow. They send a POST request to `/check` with two hex colors and receive a true/false response.

## Golden Path 2: Manual testing via web interface

A non-technical user opens the web page, enters two hex colors, clicks Check, and reads the result.

## Golden Path 3: Health monitoring

A DevOps engineer calls `/health` to verify the service is running before routing traffic.

## Why these are valuable

The API check is the core function. The web interface makes it accessible to non-developers. The health endpoint is required for production reliability.

## E2E tests covering these paths

- API check covered by Playwright API tests
- Web interface covered by browser-based Playwright test
- Health endpoint covered by API test
