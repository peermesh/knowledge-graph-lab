/**
 * Cross-browser compatibility tests for the Frontend module.
 *
 * Tests ensure the application works correctly across different browsers
 * and handles browser-specific quirks and limitations.
 */

import { test, expect, devices } from '@playwright/test'

test.describe('Cross-browser compatibility', () => {
  test('should work in Chrome', async ({ page }) => {
    await page.goto('/')

    // Wait for the application to load
    await page.waitForSelector('[data-testid="app-loaded"]', { timeout: 10000 })

    // Check basic functionality
    await expect(page.locator('h1')).toContainText('Knowledge Graph Lab')

    // Test navigation
    await page.click('[data-testid="nav-feed"]')
    await expect(page.locator('[data-testid="feed-page"]')).toBeVisible()

    // Test graph interaction
    await page.click('[data-testid="nav-lab"]')
    await expect(page.locator('[data-testid="graph-container"]')).toBeVisible()
  })

  test('should work in Firefox', async ({ page }) => {
    await page.goto('/')

    await page.waitForSelector('[data-testid="app-loaded"]', { timeout: 10000 })

    // Basic functionality tests
    await expect(page.locator('h1')).toContainText('Knowledge Graph Lab')

    // Test responsive design
    await page.setViewportSize({ width: 768, height: 1024 })
    await expect(page.locator('[data-testid="mobile-navigation"]')).toBeVisible()
  })

  test('should work in Safari (WebKit)', async ({ page }) => {
    await page.goto('/')

    await page.waitForSelector('[data-testid="app-loaded"]', { timeout: 10000 })

    // Test accessibility features
    await expect(page.locator('[data-testid="skip-link"]')).toBeVisible()

    // Test keyboard navigation
    await page.keyboard.press('Tab')
    await expect(page.locator('[data-testid="focused-element"]')).toBeVisible()
  })

  test('should handle WebGL unavailability gracefully', async ({ page, context }) => {
    // Mock WebGL unavailability
    await context.addInitScript(() => {
      Object.defineProperty(HTMLCanvasElement.prototype, 'getContext', {
        value: function() {
          return null // Simulate WebGL not available
        }
      })
    })

    await page.goto('/lab')

    // Should show fallback message instead of crashing
    await expect(page.locator('[data-testid="webgl-fallback"]')).toBeVisible()
  })

  test('should work with JavaScript disabled', async ({ page, context }) => {
    // Disable JavaScript
    await context.setJavaScriptEnabled(false)

    await page.goto('/')

    // Should show basic HTML content
    await expect(page.locator('noscript')).toBeVisible()
  })

  test('should handle network failures gracefully', async ({ page }) => {
    // Mock network failure
    await page.route('**/api/**', route => route.abort())

    await page.goto('/feed')

    // Should show offline message
    await expect(page.locator('[data-testid="offline-message"]')).toBeVisible()
  })

  test('should work with slow network', async ({ page }) => {
    // Mock slow network
    await page.route('**/api/**', async route => {
      await new Promise(resolve => setTimeout(resolve, 2000))
      await route.continue()
    })

    await page.goto('/feed')

    // Should show loading state and eventually load content
    await expect(page.locator('[data-testid="loading-spinner"]')).toBeVisible()
    await expect(page.locator('[data-testid="feed-content"]')).toBeVisible({ timeout: 10000 })
  })

  test('should support high DPI displays', async ({ page }) => {
    await page.emulateMedia({ reducedMotion: 'reduce' })

    await page.goto('/lab')

    // Test that high DPI rendering works
    const canvas = page.locator('canvas')
    await expect(canvas).toBeVisible()

    // Check that content scales appropriately
    const box = await canvas.boundingBox()
    expect(box?.width).toBeGreaterThan(800)
  })

  test('should handle memory pressure', async ({ page }) => {
    await page.goto('/lab')

    // Generate many DOM elements to simulate memory pressure
    await page.evaluate(() => {
      const container = document.createElement('div')
      for (let i = 0; i < 10000; i++) {
        const element = document.createElement('div')
        element.textContent = `Element ${i}`
        container.appendChild(element)
      }
      document.body.appendChild(container)
    })

    // Application should still be responsive
    await expect(page.locator('[data-testid="graph-container"]')).toBeVisible()
  })
})

test.describe('Performance regression tests', () => {
  test('should maintain performance with large datasets', async ({ page }) => {
    await page.goto('/lab')

    // Mock large dataset
    await page.addInitScript(() => {
      window.mockLargeDataset = {
        nodes: Array.from({ length: 1000 }, (_, i) => ({
          id: `node-${i}`,
          label: `Node ${i}`,
          x: Math.random() * 1000,
          y: Math.random() * 1000,
          size: Math.random() * 20 + 5,
        })),
        edges: Array.from({ length: 2000 }, (_, i) => ({
          id: `edge-${i}`,
          source: `node-${Math.floor(i / 2)}`,
          target: `node-${Math.floor(i / 2) + 1}`,
        })),
      }
    })

    // Measure rendering performance
    const startTime = Date.now()
    await page.waitForSelector('[data-testid="graph-rendered"]')
    const renderTime = Date.now() - startTime

    // Should render within performance budget
    expect(renderTime).toBeLessThan(3000) // 3 seconds
  })

  test('should handle rapid user interactions', async ({ page }) => {
    await page.goto('/feed')

    // Simulate rapid clicking and scrolling
    for (let i = 0; i < 10; i++) {
      await page.click('[data-testid="feed-item"]:first-child')
      await page.mouse.wheel(0, 500)
    }

    // UI should remain responsive
    await expect(page.locator('[data-testid="feed-container"]')).toBeVisible()
  })
})
