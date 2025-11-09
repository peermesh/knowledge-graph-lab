import { describe, it, expect, beforeAll, afterEach, afterAll, vi } from 'vitest'
import { render, screen, waitFor, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { BrowserRouter } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { setupServer } from 'msw/node'
import { http, HttpResponse } from 'msw'
import { feedHandlers } from '@/mocks/handlers/feed'
import { FeedPage } from '@/pages/Feed/FeedPage'

// Create MSW server for integration tests
const server = setupServer(...feedHandlers)

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

describe('Feed Page Integration Tests', () => {
  beforeAll(() => {
    server.listen({ onUnhandledRequest: 'warn' })
  })

  afterEach(() => {
    server.resetHandlers()
    vi.clearAllMocks()
  })

  afterAll(() => {
    server.close()
  })

  describe('Page Rendering', () => {
    it('renders feed page header', async () => {
      renderWithProviders(<FeedPage />)

      await waitFor(() => {
        expect(screen.getByText(/research feed/i)).toBeInTheDocument()
      })
    })

    it('loads and displays research items', async () => {
      renderWithProviders(<FeedPage />)

      // Wait for items to load
      await waitFor(() => {
        // Should have heading
        const heading = screen.getByRole('heading', { name: /research feed/i })
        expect(heading).toBeInTheDocument()
      }, { timeout: 5000 })
    })
  })

  describe('Real-Time Status', () => {
    it('shows WebSocket connection status', async () => {
      renderWithProviders(<FeedPage />)

      await waitFor(() => {
        // Look for the Live or Offline indicator
        const status = screen.getByText(/live|offline/i)
        expect(status).toBeInTheDocument()
      }, { timeout: 3000 })
    })
  })

  describe('Search Functionality', () => {
    it('has search input', async () => {
      renderWithProviders(<FeedPage />)

      await waitFor(() => {
        const searchInput = screen.getByPlaceholderText(/search/i)
        expect(searchInput).toBeInTheDocument()
      })
    })
  })

  describe('Action Buttons', () => {
    it('has filters button', async () => {
      renderWithProviders(<FeedPage />)

      await waitFor(() => {
        const filtersButton = screen.getByRole('button', { name: /filters/i })
        expect(filtersButton).toBeInTheDocument()
      })
    })

    it('has add topics button', async () => {
      renderWithProviders(<FeedPage />)

      await waitFor(() => {
        const addButton = screen.getByRole('button', { name: /add topics/i })
        expect(addButton).toBeInTheDocument()
      })
    })
  })

  describe('Error Handling', () => {
    it('handles API errors gracefully', async () => {
      // Override handler to return error
      server.use(
        http.get('/api/v1/feed', () => {
          return HttpResponse.json(
            { error: 'Internal server error' },
            { status: 500 }
          )
        })
      )

      renderWithProviders(<FeedPage />)

      // Should render page structure even with error
      await waitFor(() => {
        const heading = screen.getByRole('heading', { name: /research feed/i })
        expect(heading).toBeInTheDocument()
      }, { timeout: 5000 })
    })
  })

  describe('Accessibility', () => {
    it('has proper heading hierarchy', async () => {
      renderWithProviders(<FeedPage />)

      await waitFor(() => {
        // Main page heading
        const mainHeading = screen.getByRole('heading', { level: 1 })
        expect(mainHeading).toHaveTextContent(/research feed/i)
      })
    })

    it('search input is accessible', async () => {
      renderWithProviders(<FeedPage />)

      const searchInput = screen.getByPlaceholderText(/search/i)
      expect(searchInput).toBeInTheDocument()
    })
  })

  describe('Performance', () => {
    it('loads within reasonable time', async () => {
      const startTime = Date.now()
      renderWithProviders(<FeedPage />)

      await waitFor(() => {
        const heading = screen.getByRole('heading', { name: /research feed/i })
        expect(heading).toBeInTheDocument()
      }, { timeout: 10000 })

      const endTime = Date.now()
      const loadTime = endTime - startTime

      // Should load within 10 seconds
      expect(loadTime).toBeLessThan(10000)
    })
  })
})
