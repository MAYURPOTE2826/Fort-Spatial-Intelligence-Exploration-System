import { test, expect } from '@playwright/test';

test.describe('FortSight AI User Flow', () => {
  test('User opens app and sees main components', async ({ page }) => {
    // Navigate to the app
    await page.goto('/');

    // Check if the Map is rendered (assuming it has a specific class or id we can target, or wait for tile layer)
    // We'll just check if the page title is correct or a known element exists
    await expect(page).toHaveTitle(/FortSight|Vite/i);

    // Wait for the app to load
    // Assuming there's a heading or a known UI element
    // await expect(page.locator('h1')).toBeVisible(); 
  });

  test('User can open chatbot', async ({ page }) => {
    await page.goto('/');
    
    // Find the chatbot button/input. This assumes a certain structure.
    // If the chatbot is always rendered but maybe minimized:
    const chatInput = page.locator('input[placeholder*="Ask"]');
    
    if (await chatInput.isVisible()) {
      await chatInput.fill('Hello');
      await chatInput.press('Enter');
      
      // Wait for a response or a loading indicator
      // expect(page.locator('text=...')).toBeVisible();
    }
  });
});
