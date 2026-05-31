const { test, expect } = require('@playwright/test');

test('homepage loads and shows title', async ({ page }) => {
  await page.goto('http://localhost:5000');
  await expect(page).toHaveTitle(/Color Vision Test/);
  await expect(page.locator('h1')).toContainText('Color Vision Diagnostic Test');
});

test('health endpoint returns ok', async ({ request }) => {
  const response = await request.get('http://localhost:5000/health');
  expect(response.status()).toBe(200);
  expect(await response.json()).toEqual({ status: 'ok' });
});

test('user can submit answers and complete the test', async ({ page }) => {
  await page.goto('http://localhost:5000');
  
  // Get total number of plates from the progress indicator
  const totalText = await page.locator('p').first().textContent();
  const totalMatch = totalText.match(/of (\d+)/);
  const totalPlates = totalMatch ? parseInt(totalMatch[1]) : 10;
  
  // Submit answers for all plates
  for (let i = 0; i < totalPlates; i++) {
    // Enter a guess (using 0 as default)
    await page.fill('input[name="answer"]', '0');
    await page.click('button[type="submit"]');
    await page.waitForLoadState('networkidle');
  }
  
  // Should reach results page
  await expect(page.locator('h2')).toContainText('Your Color Blind Test Result');
});

test('results page shows cone scores', async ({ page }) => {
  // Complete the test first
  await page.goto('http://localhost:5000');
  
  const totalText = await page.locator('p').first().textContent();
  const totalMatch = totalText.match(/of (\d+)/);
  const totalPlates = totalMatch ? parseInt(totalMatch[1]) : 10;
  
  for (let i = 0; i < totalPlates; i++) {
    await page.fill('input[name="answer"]', '0');
    await page.click('button[type="submit"]');
    await page.waitForLoadState('networkidle');
  }
  
  // Verify results page has score elements
  await expect(page.locator('.score').first()).toBeVisible();
});

test('reset button clears results and restarts test', async ({ page }) => {
  await page.goto('http://localhost:5000');
  
  // Complete the test
  const totalText = await page.locator('p').first().textContent();
  const totalMatch = totalText.match(/of (\d+)/);
  const totalPlates = totalMatch ? parseInt(totalMatch[1]) : 10;
  
  for (let i = 0; i < totalPlates; i++) {
    await page.fill('input[name="answer"]', '0');
    await page.click('button[type="submit"]');
    await page.waitForLoadState('networkidle');
  }
  
  // Click reset button
  await page.click('button[type="submit"]');
  
  // Should be back to first plate
  await expect(page.locator('h1')).toContainText('Color Vision Diagnostic Test');
  await expect(page.locator('input[name="answer"]')).toBeVisible();
});
