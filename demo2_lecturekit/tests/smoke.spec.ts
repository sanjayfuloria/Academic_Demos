import { test, expect } from '@playwright/test';

test('homepage loads successfully', async ({ page }) => {
  await page.goto('http://localhost:3000');
  await expect(page.locator('h1')).toContainText('LectureKit');
});

test('dashboard page loads', async ({ page }) => {
  await page.goto('http://localhost:3000/dashboard');
  await expect(page.locator('h1')).toContainText('Dashboard');
});

test('recording panel is visible', async ({ page }) => {
  await page.goto('http://localhost:3000/dashboard');
  await expect(page.locator('text=Session Recording')).toBeVisible();
});
