# Manual Testing Required

## What cannot be automated

1. **Perceptual accuracy** – An automated test cannot verify that a transformed palette actually looks distinguishable to a colorblind user. Only a human with the condition can judge that.

2. **Visual layout** – The web interface could render incorrectly (overlapping text, broken alignment) and all E2E tests would still pass because elements exist and buttons work.

3. **Error message clarity** – An automated test can check that an error message appears, but not whether it is helpful or confusing to a user.

4. **Realistic user behavior** – Automated tests follow a script. Real users do unexpected things. Manual exploratory testing catches edge cases the script misses.

## Manual test cases to run

1. Enter invalid hex formats like `#FFF` (three-digit) and `FF0000` (no hash). Does the error message make sense?

2. Use the web interface on different browsers (Chrome, Firefox, Safari). Does the layout break?

3. Ask a colorblind friend to use the tool. Do they trust the result? Is the language clear?

4. Spam the Check button rapidly. Does the UI freeze or show inconsistent results?

5. Test with very dark colors like `#001100` vs `#000011`. The API currently assumes all non-red-green pairs are distinguishable. A human would know that is not always true.
