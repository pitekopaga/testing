# Color Vision Diagnostic Test

A web-based Ishihara-style color vision test that diagnoses Protan (red deficiency), Deutan (green deficiency), and Tritan (blue deficiency) color blindness.

## Prerequisites

- Docker installed on your machine
- Git (to clone the repository)
- Node.js and npm (for E2E tests only)

## Getting Started

Clone the repository and navigate to the mock-project folder:

```bash
git clone https://github.com/pitekopaga/testing.git
cd testing/mock-project
```

## Run the Web UI

Start the application:

```bash
docker compose up --build -d
```

Open your browser and go to: `http://localhost:5000`

## How to Take the Test

1. A circle of colored dots will appear with a hidden number
2. Type the number you see in the input box
3. If you see no number, type **0**
4. Click Submit
5. Repeat for all plates
6. After the final plate, you will see your results with cone percentage scores

## Functional Requirements

| ID | Requirement | Status |
|----|-------------|--------|
| FR-1 | Present Ishihara-style dot patterns with hidden numbers | Implemented |
| FR-2 | Accept user input as a number (0-99) | Implemented |
| FR-3 | Accept "0" when user sees no number | Implemented |
| FR-4 | Track answers across all test plates | Implemented |
| FR-5 | Calculate cone response percentages for red, green, and blue | Implemented |
| FR-6 | Diagnose Protan, Deutan, or Tritan color blindness based on lowest cone score | Implemented |
| FR-7 | Provide diagnosis with description | Implemented |
| FR-8 | Allow user to reset and retake the test | Implemented |

## Non-Functional Requirements

| ID | Requirement | Status |
|----|-------------|--------|
| NFR-1 | Test completes within 2 minutes for typical users | Implemented |
| NFR-2 | Plates are generated client-side using Canvas API | Implemented |
| NFR-3 | Application runs in Docker container | Implemented |
| NFR-4 | No user data is stored permanently (session-only) | Implemented |
| NFR-5 | Test provides results with +/- 13% variance disclaimer | Implemented |
| NFR-6 | Instructions are displayed on every test page | Implemented |
| NFR-7 | Progress indicator shows current plate number and total | Implemented |
| NFR-8 | Results page shows individual cone scores with progress bars | Implemented |

## Run Automated Tests

### Unit Tests

```bash
docker compose exec api pytest unit_tests/ -v
```

### Integration Tests

```bash
docker compose exec api pytest integration_tests/ -v
```

### E2E Tests (Playwright)

```bash
npm install
npx playwright install chromium
npx playwright test
```

## Test the API manually with curl

Health check:

```bash
curl http://localhost:5000/health
```

Expected output: `{"status":"ok"}`

## Stop the Application

```bash
docker compose down
```

## Clearing Browser Data (if needed)

If the test behaves unexpectedly, clear your browser data for localhost:

**Chrome:**
1. Click the lock icon next to the address bar
2. Click "Cookies and site data"
3. Click "Manage cookies and site data"
4. Click the trash icon next to `localhost`
5. Refresh the page

**Alternative:** Open an incognito/private browsing window.

## Troubleshooting

**Port 5000 is already in use:** Stop the process using port 5000, or change the port mapping in `docker-compose.yml`.

**The test gives unexpected results:** Clear your browser data as described above.

**Playwright tests fail:** Run `npx playwright install chromium` to ensure browsers are installed.

## License

MIT
