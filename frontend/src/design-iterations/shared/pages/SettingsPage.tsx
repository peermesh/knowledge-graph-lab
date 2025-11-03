import { useState } from 'react'
import { Save, Moon, Sun, Monitor, Bell, Shield, Download, Trash2 } from 'lucide-react'

import { useUserStore } from '@/store/useUserStore'
import { useUIStore } from '@/store/useUIStore'
import { useDesignTheme } from '../ThemeProvider'
import { ThemedButton } from '../components/ThemedButton'
import { ThemedCard } from '../components/ThemedCard'

export function SharedSettingsPage() {
  const theme = useDesignTheme()
  const { user, updateUser } = useUserStore()
  const { theme: uiTheme, setTheme, addNotification } = useUIStore()

  const [formData, setFormData] = useState({
    firstName: user?.first_name || '',
    lastName: user?.last_name || '',
    email: user?.email || '',
  })

  const [preferences, setPreferences] = useState({
    emailNotifications: true,
    pushNotifications: true,
    newsletterFrequency: 'daily',
    theme: uiTheme,
    autoRefresh: true,
    refreshInterval: 30,
  })

  const handleSaveProfile = () => {
    updateUser({
      first_name: formData.firstName,
      last_name: formData.lastName,
      email: formData.email,
    })
    addNotification({ type: 'success', message: 'Profile updated successfully', duration: 3000 })
  }

  const handleSavePreferences = () => {
    setTheme(preferences.theme)
    addNotification({ type: 'success', message: 'Preferences updated successfully', duration: 3000 })
  }

  const handleExportData = () => {
    addNotification({ type: 'success', message: 'Data export initiated. You will receive an email when ready.', duration: 5000 })
  }

  const handleDeleteAccount = () => {
    addNotification({ type: 'error', message: 'Account deletion requires additional verification', duration: 5000 })
  }

  return (
    <div className="max-w-4xl mx-auto" style={{ padding: theme.spacing.xl }}>
      {/* Header */}
      <div style={{ marginBottom: theme.spacing['2xl'] }}>
        <h1
          style={{
            fontSize: theme.typography.fontSize['3xl'],
            fontWeight: theme.typography.fontWeight.bold,
            color: theme.colors.neutral[900],
          }}
        >
          Settings
        </h1>
        <p style={{ color: theme.colors.neutral[500] }}>
          Manage your account, preferences, and application settings
        </p>
      </div>

      <div className="space-y-8">
        {/* Profile Settings */}
        <ThemedCard accentBorder="none">
          <h2
            className="flex items-center gap-2"
            style={{
              fontSize: theme.typography.fontSize.xl,
              fontWeight: theme.typography.fontWeight.semibold,
              marginBottom: theme.spacing.lg,
              color: theme.colors.neutral[900],
            }}
          >
            <Shield className="w-5 h-5" style={{ color: theme.colors.primary[500] }} />
            Profile Information
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
            <div>
              <label
                className="block mb-2"
                style={{
                  fontSize: theme.typography.fontSize.sm,
                  fontWeight: theme.typography.fontWeight.medium,
                  color: theme.colors.neutral[700],
                }}
              >
                First Name
              </label>
              <input
                value={formData.firstName}
                onChange={(e) => setFormData(prev => ({ ...prev, firstName: e.target.value }))}
                placeholder="Enter your first name"
                style={{
                  width: '100%',
                  padding: '0.625rem 1rem',
                  borderRadius: theme.borderRadius.md,
                  border: `1px solid ${theme.colors.neutral[300]}`,
                  fontSize: theme.typography.fontSize.sm,
                }}
              />
            </div>

            <div>
              <label
                className="block mb-2"
                style={{
                  fontSize: theme.typography.fontSize.sm,
                  fontWeight: theme.typography.fontWeight.medium,
                  color: theme.colors.neutral[700],
                }}
              >
                Last Name
              </label>
              <input
                value={formData.lastName}
                onChange={(e) => setFormData(prev => ({ ...prev, lastName: e.target.value }))}
                placeholder="Enter your last name"
                style={{
                  width: '100%',
                  padding: '0.625rem 1rem',
                  borderRadius: theme.borderRadius.md,
                  border: `1px solid ${theme.colors.neutral[300]}`,
                  fontSize: theme.typography.fontSize.sm,
                }}
              />
            </div>

            <div className="md:col-span-2">
              <label
                className="block mb-2"
                style={{
                  fontSize: theme.typography.fontSize.sm,
                  fontWeight: theme.typography.fontWeight.medium,
                  color: theme.colors.neutral[700],
                }}
              >
                Email Address
              </label>
              <input
                type="email"
                value={formData.email}
                onChange={(e) => setFormData(prev => ({ ...prev, email: e.target.value }))}
                placeholder="Enter your email address"
                style={{
                  width: '100%',
                  padding: '0.625rem 1rem',
                  borderRadius: theme.borderRadius.md,
                  border: `1px solid ${theme.colors.neutral[300]}`,
                  fontSize: theme.typography.fontSize.sm,
                }}
              />
            </div>
          </div>

          <ThemedButton onClick={handleSaveProfile} icon={<Save className="w-4 h-4" />}>
            Save Profile
          </ThemedButton>
        </ThemedCard>

        {/* Notification Preferences */}
        <ThemedCard accentBorder="none">
          <h2
            className="flex items-center gap-2"
            style={{
              fontSize: theme.typography.fontSize.xl,
              fontWeight: theme.typography.fontWeight.semibold,
              marginBottom: theme.spacing.lg,
              color: theme.colors.neutral[900],
            }}
          >
            <Bell className="w-5 h-5" style={{ color: theme.colors.primary[500] }} />
            Notification Preferences
          </h2>

          <div className="space-y-4 mb-6">
            <div className="flex items-center justify-between">
              <div>
                <label
                  style={{
                    fontSize: theme.typography.fontSize.sm,
                    fontWeight: theme.typography.fontWeight.medium,
                    color: theme.colors.neutral[900],
                  }}
                >
                  Email Notifications
                </label>
                <p style={{ fontSize: theme.typography.fontSize.xs, color: theme.colors.neutral[500] }}>
                  Receive email updates about your research
                </p>
              </div>
              <input
                type="checkbox"
                checked={preferences.emailNotifications}
                onChange={(e) => setPreferences(prev => ({ ...prev, emailNotifications: e.target.checked }))}
                style={{ width: '1.25rem', height: '1.25rem' }}
              />
            </div>

            <div className="flex items-center justify-between">
              <div>
                <label
                  style={{
                    fontSize: theme.typography.fontSize.sm,
                    fontWeight: theme.typography.fontWeight.medium,
                    color: theme.colors.neutral[900],
                  }}
                >
                  Push Notifications
                </label>
                <p style={{ fontSize: theme.typography.fontSize.xs, color: theme.colors.neutral[500] }}>
                  Receive browser notifications for alerts
                </p>
              </div>
              <input
                type="checkbox"
                checked={preferences.pushNotifications}
                onChange={(e) => setPreferences(prev => ({ ...prev, pushNotifications: e.target.checked }))}
                style={{ width: '1.25rem', height: '1.25rem' }}
              />
            </div>
          </div>

          <ThemedButton onClick={handleSavePreferences} icon={<Save className="w-4 h-4" />}>
            Save Preferences
          </ThemedButton>
        </ThemedCard>

        {/* Appearance */}
        <ThemedCard accentBorder="none">
          <h2
            className="flex items-center gap-2"
            style={{
              fontSize: theme.typography.fontSize.xl,
              fontWeight: theme.typography.fontWeight.semibold,
              marginBottom: theme.spacing.lg,
              color: theme.colors.neutral[900],
            }}
          >
            <Monitor className="w-5 h-5" style={{ color: theme.colors.primary[500] }} />
            Appearance
          </h2>

          <div>
            <label
              className="block mb-3"
              style={{
                fontSize: theme.typography.fontSize.sm,
                fontWeight: theme.typography.fontWeight.medium,
                color: theme.colors.neutral[700],
              }}
            >
              Theme
            </label>
            <div className="flex gap-3">
              {[
                { value: 'light', icon: Sun, label: 'Light' },
                { value: 'dark', icon: Moon, label: 'Dark' },
                { value: 'auto', icon: Monitor, label: 'Auto' },
              ].map(({ value, icon: Icon, label }) => (
                <button
                  key={value}
                  onClick={() => setPreferences(prev => ({ ...prev, theme: value as any }))}
                  className="flex items-center gap-2 px-4 py-2 rounded-md border transition-colors"
                  style={{
                    borderColor: preferences.theme === value ? theme.colors.primary[500] : theme.colors.neutral[200],
                    background: preferences.theme === value ? `${theme.colors.primary[500]}1A` : 'white',
                    color: preferences.theme === value ? theme.colors.primary[700] : theme.colors.neutral[600],
                  }}
                >
                  <Icon className="w-4 h-4" />
                  <span style={{ fontSize: theme.typography.fontSize.sm }}>{label}</span>
                </button>
              ))}
            </div>
          </div>
        </ThemedCard>

        {/* Data Management */}
        <ThemedCard accentBorder="none">
          <h2
            className="flex items-center gap-2"
            style={{
              fontSize: theme.typography.fontSize.xl,
              fontWeight: theme.typography.fontWeight.semibold,
              marginBottom: theme.spacing.lg,
              color: theme.colors.neutral[900],
            }}
          >
            <Download className="w-5 h-5" style={{ color: theme.colors.primary[500] }} />
            Data Management
          </h2>

          <div className="space-y-4">
            <div
              className="flex items-center justify-between p-4 rounded-lg"
              style={{ background: theme.colors.neutral[100] }}
            >
              <div>
                <h3 style={{ fontWeight: theme.typography.fontWeight.medium }}>Export Your Data</h3>
                <p style={{ fontSize: theme.typography.fontSize.sm, color: theme.colors.neutral[500] }}>
                  Download all your research items, saved content, and preferences
                </p>
              </div>
              <ThemedButton variant="outline" onClick={handleExportData} icon={<Download className="w-4 h-4" />}>
                Export Data
              </ThemedButton>
            </div>

            <div
              className="flex items-center justify-between p-4 rounded-lg"
              style={{ background: '#FEE2E2', border: '1px solid #FCA5A5' }}
            >
              <div>
                <h3 style={{ fontWeight: theme.typography.fontWeight.medium, color: '#991B1B' }}>Danger Zone</h3>
                <p style={{ fontSize: theme.typography.fontSize.sm, color: '#7F1D1D' }}>
                  Permanently delete your account and all associated data
                </p>
              </div>
              <button
                onClick={handleDeleteAccount}
                className="flex items-center gap-2 px-4 py-2 rounded-lg font-semibold"
                style={{
                  background: '#DC2626',
                  color: 'white',
                  fontSize: theme.typography.fontSize.sm,
                }}
              >
                <Trash2 className="w-4 h-4" />
                Delete Account
              </button>
            </div>
          </div>
        </ThemedCard>

        {/* Footer */}
        <div className="text-center" style={{ fontSize: theme.typography.fontSize.sm, color: theme.colors.neutral[500] }}>
          <p>Knowledge Graph Lab v1.0.0</p>
          <p>Built with React, TypeScript, and Tailwind CSS</p>
        </div>
      </div>
    </div>
  )
}

