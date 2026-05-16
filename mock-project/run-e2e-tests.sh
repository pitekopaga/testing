#!/bin/bash
# Start the API
docker compose up --build -d

# Wait for API to be ready
sleep 5

# Run Playwright tests
npx playwright test

# Capture exit code
EXIT_CODE=$?

# Stop containers
docker compose down

# Exit with Playwright's exit code
exit $EXIT_CODE
