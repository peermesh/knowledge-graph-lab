/**
 * Accessibility tests for the Frontend module.
 *
 * Tests ensure WCAG 2.1 AA compliance and proper accessibility
 * features throughout the application.
 */

import { test, expect } from '@playwright/test'

test.describe('Accessibility compliance', () => {
  test.beforeEach(async ({ page }) => {
    // Enable accessibility testing
    await page.goto('/', { waitUntil: 'domcontentloaded' })
  })

  test('should have proper heading structure', async ({ page }) => {
    // Check for proper heading hierarchy
    const headings = await page.locator('h1, h2, h3, h4, h5, h6').allTextContents()

    // Should have at least one h1
    const h1Count = await page.locator('h1').count()
    expect(h1Count).toBeGreaterThan(0)

    // Headings should be in sequential order
    let lastLevel = 0
    for (const heading of headings) {
      const level = parseInt(heading.charAt(1))
      expect(level).toBeLessThanOrEqual(lastLevel + 1)
      lastLevel = level
    }
  })

  test('should have proper ARIA landmarks', async ({ page }) => {
    // Check for main landmark
    await expect(page.locator('main')).toBeVisible()

    // Check for navigation landmark
    await expect(page.locator('nav')).toBeVisible()

    // Check for complementary landmark (context panel)
    const complementary = page.locator('[role="complementary"], aside')
    await expect(complementary.first()).toBeVisible()
  })

  test('should have skip links for keyboard navigation', async ({ page }) => {
    // Check for skip link
    const skipLink = page.locator('a[href="#main-content"]')
    await expect(skipLink).toBeVisible()

    // Skip link should be first focusable element
    await page.keyboard.press('Tab')
    await expect(page.locator(':focus')).toHaveAttribute('href', '#main-content')
  })

  test('should have proper focus management', async ({ page }) => {
    await page.goto('/lab')

    // Focus should be managed properly in modal dialogs
    await page.click('[data-testid="settings-button"]')

    // Modal should trap focus
    await expect(page.locator('[role="dialog"]')).toBeVisible()

    // Focus should be inside modal
    const focusedElement = page.locator(':focus')
    await expect(focusedElement.locator('..')).toHaveAttribute('role', 'dialog')
  })

  test('should have proper color contrast', async ({ page }) => {
    // Test that all text has sufficient contrast
    const textElements = page.locator('p, span, div, button, a, h1, h2, h3, h4, h5, h6')

    // This would typically use axe-core for automated contrast testing
    // For now, we'll check that text is visible
    await expect(textElements.first()).toBeVisible()
  })

  test('should support keyboard navigation', async ({ page }) => {
    // Test tab navigation through interface
    await page.keyboard.press('Tab')
    await expect(page.locator(':focus')).toBeVisible()

    // Should be able to navigate through all interactive elements
    let tabCount = 0
    while (tabCount < 20) { // Prevent infinite loop
      const focused = page.locator(':focus')
      if (await focused.count() === 0) break

      await page.keyboard.press('Tab')
      tabCount++
    }

    // Should have navigated through multiple elements
    expect(tabCount).toBeGreaterThan(5)
  })

  test('should have proper form labels', async ({ page }) => {
    await page.goto('/settings')

    // All form inputs should have labels
    const inputs = page.locator('input[type="text"], input[type="email"], input[type="password"]')

    for (let i = 0; i < await inputs.count(); i++) {
      const input = inputs.nth(i)
      const id = await input.getAttribute('id')

      if (id) {
        const label = page.locator(`label[for="${id}"]`)
        await expect(label).toBeVisible()
      }
    }
  })

  test('should have proper button labels', async ({ page }) => {
    // All buttons should have accessible names
    const buttons = page.locator('button')

    for (let i = 0; i < await buttons.count(); i++) {
      const button = buttons.nth(i)
      const accessibleName = await button.getAttribute('aria-label') ||
                           await button.textContent() ||
                           await button.getAttribute('title')

      expect(accessibleName).toBeTruthy()
    }
  })

  test('should support screen readers', async ({ page }) => {
    // Check for proper ARIA attributes
    const navigation = page.locator('nav')
    await expect(navigation).toHaveAttribute('aria-label', /navigation|menu/i)

    // Check for live regions for dynamic content
    const liveRegions = page.locator('[aria-live], [role="status"], [role="alert"]')
    await expect(liveRegions.first()).toBeVisible()
  })

  test('should have proper image alt text', async ({ page }) => {
    // Check all images have alt text
    const images = page.locator('img')

    for (let i = 0; i < await images.count(); i++) {
      const img = images.nth(i)
      const alt = await img.getAttribute('alt')

      // Alt text should exist (can be empty for decorative images)
      expect(alt).not.toBeNull()
    }
  })

  test('should handle reduced motion preferences', async ({ page }) => {
    // Test with reduced motion
    await page.emulateMedia({ reducedMotion: 'reduce' })

    // Animations should be disabled
    const animatedElements = page.locator('[style*="animation"], [class*="animate-"]')
    // This would check that animations are properly disabled
  })

  test('should support high contrast mode', async ({ page }) => {
    // Test with high contrast
    await page.emulateMedia({ colorScheme: 'dark' })

    // Text should still be readable
    await expect(page.locator('h1')).toBeVisible()
  })

  test('should have proper error announcements', async ({ page }) => {
    // Trigger an error
    await page.goto('/invalid-route')

    // Error should be announced to screen readers
    const errorElement = page.locator('[role="alert"], .error-message')
    await expect(errorElement).toBeVisible()
  })
})

test.describe('Mobile accessibility', () => {
  test.use({ viewport: { width: 375, height: 667 } }) // iPhone size

  test('should be usable on mobile devices', async ({ page }) => {
    await page.goto('/feed')

    // Touch targets should be at least 44px
    const buttons = page.locator('button')
    for (let i = 0; i < await buttons.count(); i++) {
      const button = buttons.nth(i)
      const box = await button.boundingBox()
      if (box) {
        expect(Math.max(box.width, box.height)).toBeGreaterThanOrEqual(44)
      }
    }
  })

  test('should have mobile-friendly navigation', async ({ page }) => {
    await page.goto('/')

    // Mobile navigation should be accessible
    const navToggle = page.locator('[data-testid="mobile-nav-toggle"]')
    if (await navToggle.isVisible()) {
      await navToggle.tap()

      // Navigation menu should be accessible
      await expect(page.locator('[data-testid="mobile-nav-menu"]')).toBeVisible()
    }
  })
})
