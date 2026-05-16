# Manual Testing Required Beyond Automation

## What cannot be automated

1. **Diagnostic accuracy** – An automated test cannot verify that the diagnosis matches a clinical test like Enchroma. Only a human with known color blindness can validate this.

2. **Perceptual difficulty calibration** – The test needs to be challenging but not impossible. Automated tests only check that the flow completes, not that the colors are properly calibrated.

3. **User experience** – An automated test cannot judge whether the instructions are clear, the interface is intuitive, or the results are easy to understand.

4. **Realistic user behavior** – Automated tests follow a script (typing 0 for every plate). Real users may hesitate, change answers, or behave unpredictably.

## Manual test cases to run

1. **Diagnostic accuracy** – Have a user with known color blindness (Protan, Deutan, or Tritan) take the test. Compare the results to their Enchroma or clinical diagnosis.

2. **Calibration check** – A person with normal vision should get "Normal Color Vision" consistently. If they get a false positive, the test is too hard.

3. **Variance check** – Take the test 3 times. Scores should vary within the +/- 13% disclaimer. Large swings indicate instability.

4. **Usability** – Ask a first-time user to take the test without instructions. Where do they get stuck? Is the "enter 0 if you see no number" instruction clear?

5. **Cross-browser testing** – Test on Chrome, Firefox, and Safari. The Canvas rendering should be consistent.

6. **Mobile testing** – The test is designed for desktop. On mobile, the numbers may be too small. Document this limitation.

## Manual test results template

| Test Case | Result | Notes |
|-----------|--------|-------|
| Protan user diagnosis | Pending | Need test subject |
| Deutan user diagnosis | Pending | Need test subject |
| Tritan user diagnosis | Pending | Need test subject |
| Normal vision (3x) | Pending | Should get Normal each time |
| First-time usability | Pending | Observe hesitation points |
| Chrome | Pending | |
| Firefox | Pending | |
| Safari | Pending | |

## Recommendations for improvement

- Recruit colorblind users for validation
- Add a calibration mode with known control plates
- Implement a confidence score based on response consistency
