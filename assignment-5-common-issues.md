# Common Production Issues for Colorblindness Diagnostic Tools

Based on research of similar products (Enchroma, Color Blind Check, Ishihara Test apps) and SOA/REST principles:

## Functional issues

1. **False positives/negatives** – Users report inconsistent results between test sessions. The slides note that scores can vary by +/-13%, but some users experience wider swings. This is the highest-priority issue because a misdiagnosis erodes trust.

2. **Calibration issues** – Different screens (OLED vs LCD, brightness settings) affect color perception. A test calibrated on one device may be too easy or too hard on another.

3. **Scoring algorithm bugs** – A bug in the cone score calculation would misdiagnose every user. My unit tests do not currently cover this logic.

## Operational issues (from SOA statelessness principle, SRC-3, SRC-27)

4. **Session state as a bottleneck** – My application uses server-side Flask sessions to track user progress. Under load, the session store becomes a bottleneck. If a user refreshes the page or opens multiple tabs, the session can become corrupted. A stateless design would store answers in localStorage or a signed JWT, aligning with REST statelessness constraints. This would also simplify load testing because each request would be independent.

5. **No runbook for incident response** – If the test goes down at 2am, there are no documented steps for investigation or recovery.

## Accessibility issues

6. **Keyboard navigation gaps** – Users who cannot use a mouse may struggle to take the test.

7. **Screen reader support** – The canvas-based number display is not accessible to blind users. This is a fundamental limitation of the Ishihara format.

## Load/performance issues

8. **Unknown concurrency limits** – I have not tested how the system behaves under 100 concurrent users. The Flask development server is single-threaded and not production-ready.
