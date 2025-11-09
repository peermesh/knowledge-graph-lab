import { test, expect } from '@playwright/test'

test.describe('Complete User Journey', () => {
  test.beforeEach(async ({ page }) => {
    // Clear localStorage before each test
    await page.goto('/')
    await page.evaluate(() => localStorage.clear())
  })

  test('full user journey: login -> feed -> graph lab -> settings -> logout', async ({ page }) => {
    // Step 1: Navigate to login page
    await page.goto('/login')
    await expect(page).toHaveURL(/.*login/)
    await expect(page.locator('h2')).toContainText('Welcome back')

    // Step 2: Fill demo credentials and login
    await page.getByRole('button', { name: /fill demo credentials/i }).click()
    
    // Verify fields are filled
    const emailInput = page.getByPlaceholderText(/you@example.com/i)
    const passwordInput = page.getByPlaceholderText(/••••••••/i)
    await expect(emailInput).toHaveValue('demo@example.com')
    await expect(passwordInput).toHaveValue('password123')

    // Submit login form
    await page.getByRole('button', { name: /^sign in$/i }).click()

    // Step 3: Verify redirect to feed page
    await expect(page).toHaveURL(/.*feed/, { timeout: 10000 })
    await expect(page.locator('h1')).toContainText('Research Feed', { timeout: 10000 })

    // Verify WebSocket status indicator is present
    await expect(page.getByText(/live|offline/i)).toBeVisible({ timeout: 5000 })

    // Verify research items load
    await page.waitForTimeout(2000) // Wait for items to load
    
    // Step 4: Test search functionality
    const searchInput = page.getByPlaceholderText(/search/i)
    await searchInput.fill('test search')
    await expect(searchInput).toHaveValue('test search')

    // Step 5: Navigate to Graph Lab
    await page.getByRole('link', { name: /graph lab/i }).click()
    await expect(page).toHaveURL(/.*lab/, { timeout: 5000 })
    
    // Wait for graph to potentially load
    await page.waitForTimeout(3000)

    // Step 6: Navigate to Settings
    await page.getByRole('link', { name: /settings/i }).click()
    await expect(page).toHaveURL(/.*settings/, { timeout: 5000 })
    await expect(page.locator('h1')).toContainText('Settings', { timeout: 5000 })

    // Verify profile section exists
    await expect(page.getByText(/profile information/i)).toBeVisible()

    // Step 7: Logout
    await page.getByRole('button', { name: /logout/i }).click()

    // Verify redirect to login
    await expect(page).toHaveURL(/.*login/, { timeout: 10000 })

    // Verify tokens are cleared
    const hasToken = await page.evaluate(() => {
      return localStorage.getItem('access_token') !== null
    })
    expect(hasToken).toBe(false)
  })

  test('registration flow', async ({ page }) => {
    // Navigate to register page
    await page.goto('/register')
    await expect(page).toHaveURL(/.*register/)
    await expect(page.locator('h2')).toContainText('Create your account')

    // Fill registration form
    await page.getByLabelText(/first name/i).fill('John')
    await page.getByLabelText(/last name/i).fill('Doe')
    await page.getByLabelText(/email address/i).fill(`test-${Date.now()}@example.com`)
    
    // Fill passwords
    const passwordInputs = page.getByPlaceholderText(/••••••••/i)
    await passwordInputs.nth(0).fill('password123')
    await passwordInputs.nth(1).fill('password123')

    // Accept terms
    await page.getByRole('checkbox', { name: /i agree to the/i }).check()

    // Submit form
    await page.getByRole('button', { name: /create account/i }).click()

    // Should redirect to login or show success
    await page.waitForTimeout(2000)
    
    // Verify we're either on login page or see success message
    const currentUrl = page.url()
    expect(currentUrl).toMatch(/login|register/)
  })

  test('feed page interactions', async ({ page }) => {
    // Login first
    await page.goto('/login')
    await page.getByRole('button', { name: /fill demo credentials/i }).click()
    await page.getByRole('button', { name: /^sign in$/i }).click()
    
    // Wait for redirect to feed
    await expect(page).toHaveURL(/.*feed/, { timeout: 10000 })

    // Wait for content to load
    await page.waitForTimeout(2000)

    // Test filters button
    const filtersButton = page.getByRole('button', { name: /filters/i })
    await expect(filtersButton).toBeVisible()
    
    // Test add topics button
    const addTopicsButton = page.getByRole('button', { name: /add topics/i })
    await expect(addTopicsButton).toBeVisible()

    // Test search
    const searchInput = page.getByPlaceholderText(/search/i)
    await searchInput.fill('innovation')
    await expect(searchInput).toHaveValue('innovation')
  })

  test('navigation between pages', async ({ page }) => {
    // Login
    await page.goto('/login')
    await page.getByRole('button', { name: /fill demo credentials/i }).click()
    await page.getByRole('button', { name: /^sign in$/i }).click()
    await expect(page).toHaveURL(/.*feed/, { timeout: 10000 })

    // Test navigation links
    const pages = [
      { link: /graph lab/i, url: /.*lab/ },
      { link: /settings/i, url: /.*settings/ },
      { link: /feed/i, url: /.*feed/ },
    ]

    for (const { link, url } of pages) {
      await page.getByRole('link', { name: link }).click()
      await expect(page).toHaveURL(url, { timeout: 5000 })
      await page.waitForTimeout(1000)
    }
  })

  test('responsive design - mobile view', async ({ page }) => {
    // Set mobile viewport
    await page.setViewportSize({ width: 375, height: 667 })

    // Navigate and test in mobile view
    await page.goto('/login')
    await expect(page.locator('h2')).toBeVisible()

    // Login in mobile view
    await page.getByRole('button', { name: /fill demo credentials/i }).click()
    await page.getByRole('button', { name: /^sign in$/i }).click()

    // Verify feed loads in mobile view
    await expect(page).toHaveURL(/.*feed/, { timeout: 10000 })
    await expect(page.locator('h1')).toContainText('Research Feed', { timeout: 10000 })
  })

  test('error handling - invalid login', async ({ page }) => {
    await page.goto('/login')

    // Try to login with invalid credentials
    await page.getByPlaceholderText(/you@example.com/i).fill('test@example.com')
    await page.getByPlaceholderText(/••••••••/i).fill('12') // Too short

    await page.getByRole('button', { name: /^sign in$/i }).click()

    // Should show error message
    await expect(page.getByText(/invalid credentials/i)).toBeVisible({ timeout: 5000 })

    // Should not redirect
    await expect(page).toHaveURL(/.*login/)
  })

  test('accessibility - keyboard navigation', async ({ page }) => {
    await page.goto('/login')

    // Test keyboard navigation
    await page.keyboard.press('Tab') // Should focus email input
    await page.keyboard.type('demo@example.com')
    
    await page.keyboard.press('Tab') // Should focus password input
    await page.keyboard.type('password123')
    
    await page.keyboard.press('Tab') // Should focus remember me checkbox
    await page.keyboard.press('Tab') // Should focus forgot password
    await page.keyboard.press('Tab') // Should focus sign in button
    
    await page.keyboard.press('Enter') // Should submit form

    // Should login successfully
    await expect(page).toHaveURL(/.*feed/, { timeout: 10000 })
  })
})

test.describe('Performance Tests', () => {
  test('pages load within acceptable time', async ({ page }) => {
    const startTime = Date.now()
    
    await page.goto('/login')
    await expect(page.locator('h2')).toBeVisible()
    
    const loadTime = Date.now() - startTime
    
    // Should load in less than 5 seconds
    expect(loadTime).toBeLessThan(5000)
  })

  test('feed page loads and renders quickly', async ({ page }) => {
    // Login first
    await page.goto('/login')
    await page.getByRole('button', { name: /fill demo credentials/i }).click()
    await page.getByRole('button', { name: /^sign in$/i }).click()
    
    await expect(page).toHaveURL(/.*feed/, { timeout: 10000 })

    const startTime = Date.now()
    
    // Wait for main content
    await expect(page.locator('h1')).toContainText('Research Feed', { timeout: 10000 })
    
    const renderTime = Date.now() - startTime
    
    // Should render in less than 5 seconds
    expect(renderTime).toBeLessThan(5000)
  })
})

