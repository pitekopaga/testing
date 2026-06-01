# Test Plan

## Features to Test
- Valid hex color pairs
- Identical colors
- Red vs green (should fail)
- Red vs blue (should pass)
- Case insensitivity
- Invalid inputs (documented but not yet validated)

## Test Cases
See `mock-project/tests/test_colorblind.py`

## Setup Steps
1. Run `docker compose up -d` from the mock-project folder
2. Run `docker compose exec api pytest tests/ -v`

## Expected Outcomes
All tests should pass. Tests for invalid inputs are placeholders until validation is added to the function.