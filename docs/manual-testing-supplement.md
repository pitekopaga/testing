# Manual Testing Required Beyond Automation (Assignment 5)

## What cannot be automated (or was not automated)

1. **Stress testing** – Requires manual observation of degradation patterns under extreme load.
2. **Cross-browser visual validation** – Automated tests can check that the canvas renders, but not that colors appear correct on different screens.
3. **Accessibility** – Keyboard navigation and screen reader compatibility require human testing.
4. **Environmental conditions** – Screen glare, dark room, and varying brightness levels cannot be simulated.

## Manual test cases

1. **Stress test** – Run `docker compose up`, then send 100 rapid requests to `/`. Observe if the server crashes or slows down.
2. **Cross-browser** – Test on Chrome, Firefox, Safari. Verify canvas rendering and number visibility.
3. **Session isolation** – Open two browser tabs, take the test in tab 1, then tab 2. Verify that sessions are independent.
4. **Statelessness check** – After completing the test, refresh the page. The user should have to start over. Document whether this is acceptable.
5. **Monitoring endpoint** – Visit `/debug/stats` and verify CPU/memory readings look plausible.
6. **Keyboard navigation** – Tab through all inputs and buttons. Verify you can submit with Enter.
7. **Screen reader** – Use NVDA (Windows) or VoiceOver (Mac) to navigate the test. Note any confusing announcements.
