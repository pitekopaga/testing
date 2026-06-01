# CI Troubleshooting and Maintenance Reflection

## Designing Testable Software

My color vision diagnostic test was designed with testability in mind from the start. Key decisions included:

1. **Separation of concerns**: The backend API is separate from the frontend rendering, allowing unit tests to target the scoring logic without needing a browser.

2. **Stateless endpoints where possible**: The health and debug endpoints have no side effects, making them easy to test in isolation.

3. **Docker containerization**: The entire application runs in a container, ensuring consistent test environments across local development and CI.

## CI Pipeline Design

My GitHub Actions workflow runs three parallel jobs:
- Unit tests (pytest)
- E2E tests (Playwright)
- Load tests (Locust)

This parallelization provides fast feedback while ensuring comprehensive coverage.

## Issues Encountered and Resolved

1. **Missing docker-compose.yml in git**: The CI runner could not find the compose file because it was not committed. Fixed by adding all mock-project files to git.

2. **Playwright browsers not installed**: The CI environment did not have Chromium. Fixed by adding `npx playwright install chromium` to the workflow.

3. **Locust not available in CI**: The load test job failed because locust was not installed. Fixed by adding `pip install locust` to the workflow.

4. **Package-lock.json missing**: The E2E tests required a lock file for `npm ci`. Fixed by committing `package-lock.json`.

5. **E2E tests failing after login flow added**: The tests expected the old API format. Fixed by rewriting the Playwright tests to handle the login screen and "No Number" button.

## Lessons Learned

- Always commit all files needed to run your application, including Docker configuration and lock files.
- CI environments are not your local machine. Test your workflows with a clean runner before relying on them.
- When you change the user interface, update your automated tests immediately.
- Merging pull requests to main keeps the main branch current and avoids drift between branches.

## Maintaining Testability

As the project evolved from a simple API to a full web application with login and history tracking, I maintained testability by:

- Keeping the scoring logic independent of the session management
- Using environment variables for configuration
- Exposing health and debug endpoints for operational monitoring
- Writing tests that target specific functions, not just the full application flow
