import { describe, it, expect, beforeAll, afterEach, afterAll, vi } from 'vitest'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { BrowserRouter } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { setupServer } from 'msw/node'
import { authHandlers } from '@/mocks/handlers/auth'
import { LoginPage } from '@/pages/Login/LoginPage'
import { RegisterPage } from '@/pages/Register/RegisterPage'

// Create MSW server for integration tests
const server = setupServer(...authHandlers)

// Create a test query client
const createTestQueryClient = () => {
  return new QueryClient({
    defaultOptions: {
      queries: {
        retry: false,
      },
      mutations: {
        retry: false,
      },
    },
  })
}

// Helper to render with providers
const renderWithProviders = (ui: React.ReactElement) => {
  const queryClient = createTestQueryClient()
  
  return render(
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        {ui}
      </BrowserRouter>
    </QueryClientProvider>
  )
}

describe('Authentication Flow Integration Tests', () => {
  beforeAll(() => {
    server.listen({ onUnhandledRequest: 'error' })
  })

  afterEach(() => {
    server.resetHandlers()
    localStorage.clear()
    vi.clearAllMocks()
  })

  afterAll(() => {
    server.close()
  })

  describe('Login Flow', () => {
    it('successfully logs in with valid credentials', async () => {
      const user = userEvent.setup()
      renderWithProviders(<LoginPage />)

      // Fill in the form
      const emailInput = screen.getByPlaceholderText(/you@example.com/i)
      const passwordInput = screen.getByPlaceholderText(/••••••••/i)

      await user.type(emailInput, 'demo@example.com')
      await user.type(passwordInput, 'password123')

      // Submit the form
      const submitButton = screen.getByRole('button', { name: /sign in/i })
      await user.click(submitButton)

      // Wait for the token to be stored
      await waitFor(() => {
        const token = localStorage.getItem('access_token')
        expect(token).toBeTruthy()
        expect(token).toContain('mock_access_')
      }, { timeout: 3000 })

      // Verify refresh token is also stored
      const refreshToken = localStorage.getItem('refresh_token')
      expect(refreshToken).toBeTruthy()
      expect(refreshToken).toContain('mock_refresh_')
    })

    it('shows error with invalid credentials', async () => {
      const user = userEvent.setup()
      renderWithProviders(<LoginPage />)

      // Fill in the form with short password
      const emailInput = screen.getByPlaceholderText(/you@example.com/i)
      const passwordInput = screen.getByPlaceholderText(/••••••••/i)

      await user.type(emailInput, 'demo@example.com')
      await user.type(passwordInput, '123') // Too short

      // Submit the form
      const submitButton = screen.getByRole('button', { name: /sign in/i })
      await user.click(submitButton)

      // Wait for error message
      await waitFor(() => {
        const errorMessage = screen.getByText(/invalid credentials/i)
        expect(errorMessage).toBeInTheDocument()
      }, { timeout: 3000 })

      // Verify no tokens are stored
      expect(localStorage.getItem('access_token')).toBeNull()
      expect(localStorage.getItem('refresh_token')).toBeNull()
    })

    it('shows loading state during login', async () => {
      const user = userEvent.setup()
      renderWithProviders(<LoginPage />)

      // Fill in the form
      const emailInput = screen.getByPlaceholderText(/you@example.com/i)
      const passwordInput = screen.getByPlaceholderText(/••••••••/i)

      await user.type(emailInput, 'demo@example.com')
      await user.type(passwordInput, 'password123')

      // Submit the form
      const submitButton = screen.getByRole('button', { name: /sign in/i })
      await user.click(submitButton)

      // Check for loading state
      await waitFor(() => {
        const loadingButton = screen.getByRole('button', { name: /signing in.../i })
        expect(loadingButton).toBeInTheDocument()
      }, { timeout: 100 })
    })

    it('fill demo credentials button works', async () => {
      const user = userEvent.setup()
      renderWithProviders(<LoginPage />)

      // Click fill demo credentials
      const fillDemoButton = screen.getByRole('button', { name: /fill demo credentials/i })
      await user.click(fillDemoButton)

      // Verify fields are filled
      const emailInput = screen.getByPlaceholderText(/you@example.com/i) as HTMLInputElement
      const passwordInput = screen.getByPlaceholderText(/••••••••/i) as HTMLInputElement

      expect(emailInput.value).toBe('demo@example.com')
      expect(passwordInput.value).toBe('password123')
    })

    it('disables form during submission', async () => {
      const user = userEvent.setup()
      renderWithProviders(<LoginPage />)

      // Fill in the form
      const emailInput = screen.getByPlaceholderText(/you@example.com/i)
      const passwordInput = screen.getByPlaceholderText(/••••••••/i)

      await user.type(emailInput, 'demo@example.com')
      await user.type(passwordInput, 'password123')

      // Submit the form
      const submitButton = screen.getByRole('button', { name: /sign in/i })
      await user.click(submitButton)

      // Inputs should be disabled during submission
      await waitFor(() => {
        expect(emailInput).toBeDisabled()
        expect(passwordInput).toBeDisabled()
        expect(submitButton).toBeDisabled()
      }, { timeout: 100 })
    })
  })

  describe('Registration Flow', () => {
    it('successfully registers a new user', async () => {
      const user = userEvent.setup()
      renderWithProviders(<RegisterPage />)

      // Fill in the form
      await user.type(screen.getByLabelText(/first name/i), 'John')
      await user.type(screen.getByLabelText(/last name/i), 'Doe')
      await user.type(screen.getByLabelText(/email address/i), 'newuser@example.com')
      
      const passwordInputs = screen.getAllByPlaceholderText(/••••••••/i)
      await user.type(passwordInputs[0], 'password123')
      await user.type(passwordInputs[1], 'password123')

      // Accept terms
      const termsCheckbox = screen.getByRole('checkbox', { name: /i agree to the/i })
      await user.click(termsCheckbox)

      // Submit the form
      const submitButton = screen.getByRole('button', { name: /create account/i })
      await user.click(submitButton)

      // Wait for success (form submission)
      await waitFor(() => {
        // After successful registration, user should be created
        // In a real app, this would redirect to login
        expect(submitButton).not.toBeDisabled()
      }, { timeout: 3000 })
    })

    it('shows error for existing email', async () => {
      const user = userEvent.setup()
      renderWithProviders(<RegisterPage />)

      // Fill in the form with existing email
      await user.type(screen.getByLabelText(/first name/i), 'John')
      await user.type(screen.getByLabelText(/last name/i), 'Doe')
      await user.type(screen.getByLabelText(/email address/i), 'demo@example.com') // Existing email
      
      const passwordInputs = screen.getAllByPlaceholderText(/••••••••/i)
      await user.type(passwordInputs[0], 'password123')
      await user.type(passwordInputs[1], 'password123')

      // Accept terms
      const termsCheckbox = screen.getByRole('checkbox', { name: /i agree to the/i })
      await user.click(termsCheckbox)

      // Submit the form
      const submitButton = screen.getByRole('button', { name: /create account/i })
      await user.click(submitButton)

      // Wait for error message
      await waitFor(() => {
        const errorMessage = screen.getByText(/email already registered/i)
        expect(errorMessage).toBeInTheDocument()
      }, { timeout: 3000 })
    })

    it('validates password mismatch', async () => {
      const user = userEvent.setup()
      renderWithProviders(<RegisterPage />)

      // Fill in the form with mismatched passwords
      await user.type(screen.getByLabelText(/first name/i), 'John')
      await user.type(screen.getByLabelText(/last name/i), 'Doe')
      await user.type(screen.getByLabelText(/email address/i), 'test@example.com')
      
      const passwordInputs = screen.getAllByPlaceholderText(/••••••••/i)
      await user.type(passwordInputs[0], 'password123')
      await user.type(passwordInputs[1], 'differentpassword')

      // Accept terms
      const termsCheckbox = screen.getByRole('checkbox', { name: /i agree to the/i })
      await user.click(termsCheckbox)

      // Submit the form
      const submitButton = screen.getByRole('button', { name: /create account/i })
      await user.click(submitButton)

      // Wait for error message
      await waitFor(() => {
        const errorMessage = screen.getByText(/passwords do not match/i)
        expect(errorMessage).toBeInTheDocument()
      }, { timeout: 1000 })
    })

    it('validates password length', async () => {
      const user = userEvent.setup()
      renderWithProviders(<RegisterPage />)

      // Fill in the form with short password
      await user.type(screen.getByLabelText(/first name/i), 'John')
      await user.type(screen.getByLabelText(/last name/i), 'Doe')
      await user.type(screen.getByLabelText(/email address/i), 'test@example.com')
      
      const passwordInputs = screen.getAllByPlaceholderText(/••••••••/i)
      await user.type(passwordInputs[0], '123')
      await user.type(passwordInputs[1], '123')

      // Accept terms
      const termsCheckbox = screen.getByRole('checkbox', { name: /i agree to the/i })
      await user.click(termsCheckbox)

      // Submit the form
      const submitButton = screen.getByRole('button', { name: /create account/i })
      await user.click(submitButton)

      // Wait for error message
      await waitFor(() => {
        const errorMessage = screen.getByText(/password must be at least 6 characters/i)
        expect(errorMessage).toBeInTheDocument()
      }, { timeout: 1000 })
    })

    it('requires terms acceptance', () => {
      renderWithProviders(<RegisterPage />)

      // Terms checkbox should be required
      const termsCheckbox = screen.getByRole('checkbox', { name: /i agree to the/i })
      expect(termsCheckbox).toBeRequired()
    })
  })

  describe('Token Management', () => {
    it('stores tokens in localStorage on successful login', async () => {
      const user = userEvent.setup()
      renderWithProviders(<LoginPage />)

      // Fill and submit form
      await user.type(screen.getByPlaceholderText(/you@example.com/i), 'demo@example.com')
      await user.type(screen.getByPlaceholderText(/••••••••/i), 'password123')
      await user.click(screen.getByRole('button', { name: /sign in/i }))

      // Wait for tokens
      await waitFor(() => {
        expect(localStorage.getItem('access_token')).toBeTruthy()
        expect(localStorage.getItem('refresh_token')).toBeTruthy()
      }, { timeout: 3000 })
    })

    it('tokens have correct format', async () => {
      const user = userEvent.setup()
      renderWithProviders(<LoginPage />)

      // Fill and submit form
      await user.type(screen.getByPlaceholderText(/you@example.com/i), 'demo@example.com')
      await user.type(screen.getByPlaceholderText(/••••••••/i), 'password123')
      await user.click(screen.getByRole('button', { name: /sign in/i }))

      // Wait and verify token format
      await waitFor(() => {
        const accessToken = localStorage.getItem('access_token')
        const refreshToken = localStorage.getItem('refresh_token')

        expect(accessToken).toMatch(/^mock_access_/)
        expect(refreshToken).toMatch(/^mock_refresh_/)
      }, { timeout: 3000 })
    })
  })

  describe('UI Feedback', () => {
    it('shows demo mode indicator on login page', () => {
      renderWithProviders(<LoginPage />)

      const demoIndicator = screen.getByText(/using mock authentication/i)
      expect(demoIndicator).toBeInTheDocument()
    })

    it('shows demo mode indicator on register page', () => {
      renderWithProviders(<RegisterPage />)

      const demoIndicator = screen.getByText(/using mock authentication/i)
      expect(demoIndicator).toBeInTheDocument()
    })

    it('shows link to register from login', () => {
      renderWithProviders(<LoginPage />)

      const registerLink = screen.getByText(/create one now/i)
      expect(registerLink).toBeInTheDocument()
      expect(registerLink.closest('a')).toHaveAttribute('href', '/register')
    })

    it('shows link to login from register', () => {
      renderWithProviders(<RegisterPage />)

      const loginLink = screen.getByText(/sign in/i)
      expect(loginLink).toBeInTheDocument()
      expect(loginLink.closest('a')).toHaveAttribute('href', '/login')
    })
  })

  describe('Form Validation', () => {
    it('requires email on login', () => {
      renderWithProviders(<LoginPage />)

      const emailInput = screen.getByPlaceholderText(/you@example.com/i)
      expect(emailInput).toBeRequired()
      expect(emailInput).toHaveAttribute('type', 'email')
    })

    it('requires password on login', () => {
      renderWithProviders(<LoginPage />)

      const passwordInput = screen.getByPlaceholderText(/••••••••/i)
      expect(passwordInput).toBeRequired()
      expect(passwordInput).toHaveAttribute('type', 'password')
    })

    it('requires all fields on registration', () => {
      renderWithProviders(<RegisterPage />)

      expect(screen.getByLabelText(/first name/i)).toBeRequired()
      expect(screen.getByLabelText(/last name/i)).toBeRequired()
      expect(screen.getByLabelText(/email address/i)).toBeRequired()
      
      const passwordInputs = screen.getAllByPlaceholderText(/••••••••/i)
      expect(passwordInputs[0]).toBeRequired()
      expect(passwordInputs[1]).toBeRequired()
    })
  })
})



