import { test, expect } from '@playwright/test';

test('App loads and displays map and UI elements', async ({ page }) => {
  // Mock geolocation permission
  await page.context().grantPermissions(['geolocation']);
  
  await page.goto('/');

  // Check if title is visible
  await expect(page.locator('text=FortSight')).toBeVisible();

  // Initially we should see permission dialog if permissions are not granted 
  // or it might auto-grant depending on context mock.
  
  // Verify map container exists
  const mapContainer = page.locator('.leaflet-container');
  await expect(mapContainer).toBeVisible();
});
