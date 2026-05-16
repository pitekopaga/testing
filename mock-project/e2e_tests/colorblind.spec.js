const { test, expect } = require('@playwright/test');

test('homepage loads and shows title', async ({ page }) => {
  await page.goto('http://localhost:5000');
  await expect(page).toHaveTitle(/Colorblindness Checker Demo/);
});

test('health endpoint returns ok', async ({ request }) => {
  const response = await request.get('http://localhost:5000/health');
  expect(response.status()).toBe(200);
  expect(await response.json()).toEqual({ status: 'ok' });
});

test('red vs green returns false', async ({ request }) => {
  const response = await request.post('http://localhost:5000/check', {
    data: { color1: '#FF0000', color2: '#00FF00' }
  });
  expect(response.status()).toBe(200);
  expect(await response.json()).toEqual({ distinguishable: false });
});

test('red vs blue returns true', async ({ request }) => {
  const response = await request.post('http://localhost:5000/check', {
    data: { color1: '#FF0000', color2: '#0000FF' }
  });
  expect(response.status()).toBe(200);
  expect(await response.json()).toEqual({ distinguishable: true });
});

test('full user flow via web interface', async ({ page }) => {
  await page.goto('http://localhost:5000');
  
  // Fill in colors
  await page.fill('#color1', '#FF0000');
  await page.fill('#color2', '#00FF00');
  
  // Click check button
  await page.click('button');
  
  // Wait for result and verify
  await expect(page.locator('.result')).toContainText('NOT DISTINGUISHABLE');
  
  // Change to red and blue
  await page.fill('#color2', '#0000FF');
  await page.click('button');
  await expect(page.locator('.result')).toContainText('DISTINGUISHABLE');
});
