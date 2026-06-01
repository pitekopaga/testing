const { test, expect } = require('@playwright/test');

test('login screen loads', async ({ page }) => {
  await page.goto('http://localhost:5000');
  await expect(page.locator('h1')).toContainText('Color Vision Diagnostic Test');
  await expect(page.locator('input[name="username"]')).toBeVisible();
});

test('user can log in and start test', async ({ page }) => {
  await page.goto('http://localhost:5000');
  await page.fill('input[name="username"]', 'testuser');
  await page.click('button[type="submit"]');
  await expect(page.locator('canvas')).toBeVisible();
  await expect(page.locator('input[name="answer"]')).toBeVisible();
});

test('user can submit answers and complete the test', async ({ page }) => {
  await page.goto('http://localhost:5000');
  await page.fill('input[name="username"]', 'testuser');
  await page.click('button[type="submit"]');
  
  // Get total number of plates
  const totalText = await page.locator('p').first().textContent();
  const totalMatch = totalText.match(/of (\d+)/);
  const totalPlates = totalMatch ? parseInt(totalMatch[1]) : 18;
  
  // Submit answers for all plates
  for (let i = 0; i < totalPlates; i++) {
    await page.click('button[name="skip"]');
    await page.waitForLoadState('networkidle');
  }
  
  // Should reach results page
  await expect(page.locator('h2')).toContainText('Your Color Blind Test Result');
});

test('results page shows cone scores', async ({ page }) => {
  await page.goto('http://localhost:5000');
  await page.fill('input[name="username"]', 'testuser2');
  await page.click('button[type="submit"]');
  
  const totalText = await page.locator('p').first().textContent();
  const totalMatch = totalText.match(/of (\d+)/);
  const totalPlates = totalMatch ? parseInt(totalMatch[1]) : 18;
  
  for (let i = 0; i < totalPlates; i++) {
    await page.click('button[name="skip"]');
    await page.waitForLoadState('networkidle');
  }
  
  await expect(page.locator('.score').first()).toBeVisible();
});

test('exit button logs out and returns to login', async ({ page }) => {
  await page.goto('http://localhost:5000');
  await page.fill('input[name="username"]', 'testuser3');
  await page.click('button[type="submit"]');
  
  const totalText = await page.locator('p').first().textContent();
  const totalMatch = totalText.match(/of (\d+)/);
  const totalPlates = totalMatch ? parseInt(totalMatch[1]) : 18;
  
  for (let i = 0; i < totalPlates; i++) {
    await page.click('button[name="skip"]');
    await page.waitForLoadState('networkidle');
  }
  
  // Click the Exit button (the logout button)
  await page.click('form[action="/logout"] button');
  
  // Should return to login screen
  await expect(page.locator('input[name="username"]')).toBeVisible();
});
