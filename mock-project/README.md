# Color Vision Diagnostic Test

A web-based Ishihara-style color vision test that diagnoses Protan (red deficiency), Deutan (green deficiency), and Tritan (blue deficiency) color blindness. The test tracks your history and shows consistency across multiple sessions.

## Quick Start (for beginners)

1. Install Docker from https://docs.docker.com/get-docker/
2. Open a terminal in this folder (`mock-project`)
3. Run: `docker compose up --build -d`
4. Open your browser to: `http://localhost:5000`
5. To stop: `docker compose down`

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

1. Enter your name or email on the login screen. This saves your results for future sessions.
2. Click "Start Test".
3. A circle of colored dots will appear with a hidden number.
4. Type the number you see in the input box and press Enter, or click Submit.
5. If you see no number, click the **No Number** button.
6. Repeat for all plates (about 18 plates).
7. After the final plate, you will see your results with cone percentage scores.

## Viewing Your History

After taking the test multiple times with the same name, the results page will show:
- How many times you have taken the test
- Your consistency score (how often you get the same diagnosis)
- Your most common diagnosis
- A list of all your diagnoses from each session

## Exporting Your Results

Click the "Export All Results to CSV" button on the results page to download a file containing your complete test history with timestamps.

## Optional Survey

After viewing your results, you can click "Help Improve Accuracy (Optional Survey)" to provide feedback. The survey asks about your prior beliefs, confidence in the results, and which cone scores seemed accurate or inaccurate.

To retrieve survey responses (stored inside the Docker container):

```bash
docker compose cp api:/app/survey_data.csv backend/survey_data.csv
```

The CSV file will be saved to `backend/survey_data.csv`. Each row includes:
- Timestamp
- Username
- Test diagnosis and cone scores
- Survey answers (prior belief, confidence, accuracy feedback, etc.)

Use this data to analyze calibration accuracy and improve the test.

## Exiting and Switching Users

Click the "Exit" button to log out. The next person who uses the browser will be asked to enter their name before starting a new test.

## Functional Requirements

| ID | Requirement | Status |
|----|-------------|--------|
| FR-1 | Present Ishihara-style dot patterns with hidden numbers | Implemented |
| FR-2 | Accept user input as a number or "No Number" button | Implemented |
| FR-3 | Track answers across all test plates | Implemented |
| FR-4 | Calculate cone response percentages for red, green, and blue | Implemented |
| FR-5 | Diagnose Protan, Deutan, or Tritan color blindness | Implemented |
| FR-6 | Save results per user across sessions | Implemented |
| FR-7 | Show consistency score across multiple test sessions | Implemented |
| FR-8 | Export all user results to CSV with timestamps | Implemented |
| FR-9 | Allow user to reset and retake the test | Implemented |
| FR-10 | Allow user to log out and switch accounts | Implemented |

## Non-Functional Requirements

| ID | Requirement | Status |
|----|-------------|--------|
| NFR-1 | Test completes within 2 minutes for typical users | Implemented |
| NFR-2 | Plates are generated client-side using Canvas API | Implemented |
| NFR-3 | Application runs in Docker container | Implemented |
| NFR-4 | User data persists in JSON file between container restarts | Implemented |
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

**My results were not saved:** Make sure you entered the same name each time. Names are case-sensitive.

**Playwright tests fail:** Run `npx playwright install chromium` to ensure browsers are installed.

## License

MIT
