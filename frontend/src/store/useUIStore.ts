import { create } from 'zustand'
import { devtools, persist } from 'zustand/middleware'

import type { UIState, AppNotification } from '@/types'

interface UIStore extends UIState {
  // Actions
  setTheme: (theme: 'light' | 'dark' | 'auto') => void
  toggleSidebar: () => void
  toggleRightPanel: () => void
  setLoading: (loading: boolean, message?: string) => void
  addNotification: (notification: Omit<AppNotification, 'id' | 'timestamp'>) => void
  removeNotification: (id: string) => void
  clearNotifications: () => void
  resetUI: () => void
}

const initialState: UIState = {
  theme: 'auto',
  sidebarCollapsed: false,
  rightPanelVisible: true,
  loading: {
    isActive: false,
    message: undefined,
  },
  notifications: [],
}

export const useUIStore = create<UIStore>()(
  devtools(
    persist(
      (set, get) => ({
        ...initialState,

        setTheme: (theme) => {
          set({ theme }, false, 'setTheme')
          // Apply theme to document
          const root = document.documentElement
          if (theme === 'dark') {
            root.classList.add('dark')
          } else if (theme === 'light') {
            root.classList.remove('dark')
          } else {
            // Auto theme based on system preference
            const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches
            if (prefersDark) {
              root.classList.add('dark')
            } else {
              root.classList.remove('dark')
            }
          }
        },

        toggleSidebar: () => {
          set(
            (state) => ({ sidebarCollapsed: !state.sidebarCollapsed }),
            false,
            'toggleSidebar'
          )
        },

        toggleRightPanel: () => {
          set(
            (state) => ({ rightPanelVisible: !state.rightPanelVisible }),
            false,
            'toggleRightPanel'
          )
        },

        setLoading: (isActive, message) => {
          set(
            {
              loading: {
                isActive,
                message,
              },
            },
            false,
            'setLoading'
          )
        },

        addNotification: (notificationData) => {
          const notification: AppNotification = {
            id: crypto.randomUUID(),
            timestamp: new Date().toISOString(),
            ...notificationData,
          }

          set(
            (state) => ({
              notifications: [...state.notifications, notification],
            }),
            false,
            'addNotification'
          )

          // Auto-remove notification after duration
          if (notification.duration > 0) {
            setTimeout(() => {
              get().removeNotification(notification.id)
            }, notification.duration)
          }
        },

        removeNotification: (id) => {
          set(
            (state) => ({
              notifications: state.notifications.filter((n) => n.id !== id),
            }),
            false,
            'removeNotification'
          )
        },

        clearNotifications: () => {
          set({ notifications: [] }, false, 'clearNotifications')
        },

        resetUI: () => {
          set(initialState, false, 'resetUI')
        },
      }),
      {
        name: 'ui-store',
        partialize: (state) => ({
          theme: state.theme,
          sidebarCollapsed: state.sidebarCollapsed,
          rightPanelVisible: state.rightPanelVisible,
        }),
      }
    ),
    {
      name: 'ui-store',
    }
  )
)