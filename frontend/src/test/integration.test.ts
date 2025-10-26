/**
 * Integration tests for the Frontend module.
 *
 * Tests end-to-end workflows and module interactions to ensure
 * the complete system works together correctly.
 */

import { test, expect } from '@playwright/test'

test.describe('End-to-end workflows', () => {
  test('should complete full user onboarding flow', async ({ page }) => {
    await page.goto('/onboarding')

    // Step 1: Welcome
    await expect(page.locator('[data-testid="onboarding-welcome"]')).toBeVisible()

    // Step 2: Interest selection
    await page.click('[data-testid="next-button"]')
    await expect(page.locator('[data-testid="bubble-interface"]')).toBeVisible()

    // Select some interests
    await page.click('[data-testid="interest-bubble"]:first-child')
    await page.click('[data-testid="next-button"]')

    // Step 3: Completion
    await expect(page.locator('[data-testid="onboarding-complete"]')).toBeVisible()
    await page.click('[data-testid="get-started-button"]')

    // Should redirect to feed
    await expect(page.locator('[data-testid="feed-page"]')).toBeVisible()
  })

  test('should handle complete research workflow', async ({ page }) => {
    await page.goto('/feed')

    // View research item
    await page.click('[data-testid="research-item"]:first-child')

    // Should show item details
    await expect(page.locator('[data-testid="item-details"]')).toBeVisible()

    // Save item
    await page.click('[data-testid="save-button"]')
    await expect(page.locator('[data-testid="save-success"]')).toBeVisible()

    // Navigate to lab
    await page.click('[data-testid="view-in-lab"]')
    await expect(page.locator('[data-testid="graph-lab"]')).toBeVisible()

    // Interact with graph
    await page.click('[data-testid="graph-node"]:first-child')
    await expect(page.locator('[data-testid="node-details"]')).toBeVisible()
  })

  test('should handle authentication flow', async ({ page }) => {
    // Navigate to protected route
    await page.goto('/feed')

    // Should redirect to login
    await expect(page.locator('[data-testid="login-form"]')).toBeVisible()

    // Login
    await page.fill('[data-testid="email-input"]', 'test@example.com')
    await page.fill('[data-testid="password-input"]', 'password123')
    await page.click('[data-testid="login-button"]')

    // Should redirect to feed
    await expect(page.locator('[data-testid="feed-page"]')).toBeVisible()

    // Check user menu
    await page.click('[data-testid="user-menu"]')
    await expect(page.locator('[data-testid="user-email"]')).toContainText('test@example.com')
  })

  test('should handle settings and preferences', async ({ page }) => {
    await page.goto('/settings')

    // Change theme
    await page.click('[data-testid="theme-dark"]')
    await expect(page.locator('html')).toHaveClass(/dark/)

    // Update profile
    await page.fill('[data-testid="first-name"]', 'John')
    await page.fill('[data-testid="last-name"]', 'Doe')
    await page.click('[data-testid="save-profile"]')

    await expect(page.locator('[data-testid="profile-saved"]')).toBeVisible()
  })

  test('should handle real-time updates', async ({ page }) => {
    await page.goto('/feed')

    // Mock WebSocket message
    await page.addInitScript(() => {
      window.mockWebSocketMessage = {
        type: 'entity_update',
        data: { id: 'new-entity', name: 'New Entity' },
        timestamp: new Date().toISOString(),
      }
    })

    // Check that update is processed
    await expect(page.locator('[data-testid="feed-updated"]')).toBeVisible({ timeout: 5000 })
  })
})

test.describe('Module integration', () => {
  test('should integrate with backend API', async ({ page }) => {
    await page.goto('/feed')

    // Mock API responses
    await page.route('**/api/v1/feed**', async route => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          items: [
            {
              id: '1',
              title: 'Test Research Item',
              summary: 'Test summary',
              content_type: 'article',
              quality_score: 0.95,
              relevance_score: 0.92,
              entity_tags: ['test'],
              topics: ['Test'],
              published_at: new Date().toISOString(),
              created_at: new Date().toISOString(),
              updated_at: new Date().toISOString(),
              created_by: 'test',
              is_active: true,
            },
          ],
          pagination: {
            page: 1,
            page_size: 10,
            total_count: 1,
            has_more: false,
          },
        }),
      })
    })

    await expect(page.locator('[data-testid="research-item"]')).toBeVisible()
  })

  test('should handle API failures gracefully', async ({ page }) => {
    await page.goto('/feed')

    // Mock API failure
    await page.route('**/api/v1/feed**', async route => {
      await route.abort('failed')
    })

    await expect(page.locator('[data-testid="api-error"]')).toBeVisible()
  })

  test('should maintain state across navigation', async ({ page }) => {
    await page.goto('/feed')

    // Select an item
    await page.click('[data-testid="research-item"]:first-child')

    // Navigate to lab
    await page.click('[data-testid="nav-lab"]')

    // Navigate back to feed
    await page.click('[data-testid="nav-feed"]')

    // State should be maintained
    await expect(page.locator('[data-testid="feed-page"]')).toBeVisible()
  })
})

test.describe('Performance integration', () => {
  test('should handle large datasets efficiently', async ({ page }) => {
    await page.goto('/lab')

    // Mock large dataset
    await page.addInitScript(() => {
      window.largeGraphData = {
        nodes: Array.from({ length: 1000 }, (_, i) => ({
          id: `node-${i}`,
          label: `Node ${i}`,
          x: Math.random() * 2000,
          y: Math.random() * 2000,
          size: Math.random() * 20 + 5,
        })),
        edges: Array.from({ length: 2000 }, (_, i) => ({
          id: `edge-${i}`,
          source: `node-${Math.floor(i / 2)}`,
          target: `node-${Math.floor(i / 2) + 1}`,
        })),
      }
    })

    const startTime = Date.now()
    await page.waitForSelector('[data-testid="graph-rendered"]')
    const renderTime = Date.now() - startTime

    expect(renderTime).toBeLessThan(5000) // Should render within 5 seconds
  })

  test('should maintain performance with concurrent users', async ({ page, context }) => {
    // Create multiple pages to simulate concurrent users
    const pages = await Promise.all(
      Array.from({ length: 5 }, () => context.newPage())
    )

    await Promise.all(
      pages.map(async (page) => {
        await page.goto('/feed')
        await page.waitForSelector('[data-testid="feed-loaded"]')
      })
    )

    // All pages should load successfully
    for (const page of pages) {
      await expect(page.locator('[data-testid="feed-loaded"]')).toBeVisible()
    }
  })
})
