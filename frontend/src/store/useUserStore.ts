import { create } from 'zustand'
import { devtools, persist } from 'zustand/middleware'

import type { User } from '@/types'

interface UserStore {
  user: User | null
  isAuthenticated: boolean
  isLoading: boolean
  accessToken: string | null
  refreshToken: string | null

  // Actions
  setUser: (user: User | null) => void
  setTokens: (accessToken: string | null, refreshToken: string | null) => void
  setLoading: (loading: boolean) => void
  login: (user: User, accessToken: string, refreshToken: string) => void
  logout: () => void
  refreshUser: () => Promise<void>
  updateUser: (updates: Partial<User>) => void
}

export const useUserStore = create<UserStore>()(
  devtools(
    persist(
      (set, get) => ({
        user: null,
        isAuthenticated: false,
        isLoading: false,
        accessToken: null,
        refreshToken: null,

        setUser: (user) => {
          set(
            {
              user,
              isAuthenticated: user !== null,
            },
            false,
            'setUser'
          )
        },

        setTokens: (accessToken, refreshToken) => {
          set(
            {
              accessToken,
              refreshToken,
            },
            false,
            'setTokens'
          )
        },

        setLoading: (isLoading) => {
          set({ isLoading }, false, 'setLoading')
        },

        login: (user, accessToken, refreshToken) => {
          set(
            {
              user,
              isAuthenticated: true,
              isLoading: false,
              accessToken,
              refreshToken,
            },
            false,
            'login'
          )

          // Store tokens in localStorage for API client
          localStorage.setItem('access_token', accessToken)
          localStorage.setItem('refresh_token', refreshToken)
        },

        logout: () => {
          set(
            {
              user: null,
              isAuthenticated: false,
              isLoading: false,
              accessToken: null,
              refreshToken: null,
            },
            false,
            'logout'
          )

          // Clear tokens from localStorage
          localStorage.removeItem('access_token')
          localStorage.removeItem('refresh_token')
        },

        refreshUser: async () => {
          const state = get()
          if (!state.accessToken) {
            throw new Error('No access token available')
          }

          try {
            set({ isLoading: true }, false, 'refreshUser')

            // Call API to get current user
            const user = await fetch('/api/v1/auth/me', {
              headers: {
                Authorization: `Bearer ${state.accessToken}`,
              },
            }).then((res) => res.json())

            set(
              {
                user,
                isLoading: false,
              },
              false,
              'refreshUser'
            )
          } catch (error) {
            set({ isLoading: false }, false, 'refreshUser')
            throw error
          }
        },

        updateUser: (updates) => {
          const state = get()
          if (!state.user) {
            throw new Error('No user to update')
          }

          const updatedUser = { ...state.user, ...updates }
          set({ user: updatedUser }, false, 'updateUser')
        },
      }),
      {
        name: 'user-store',
        partialize: (state) => ({
          user: state.user,
          isAuthenticated: state.isAuthenticated,
          accessToken: state.accessToken,
          refreshToken: state.refreshToken,
        }),
      }
    ),
    {
      name: 'user-store',
    }
  )
)