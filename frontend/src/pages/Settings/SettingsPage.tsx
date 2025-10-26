import { useState } from 'react'
import { Save, Moon, Sun, Monitor, Bell, Shield, Download, Trash2 } from 'lucide-react'

import { Button } from '@/components/Common/Button'
import { Input } from '@/components/Common/Input'
import { useUserStore } from '@/store/useUserStore'
import { useUIStore } from '@/store/useUIStore'

export function SettingsPage() {
  const { user, updateUser } = useUserStore()
  const { theme, setTheme, addNotification } = useUIStore()

  const [formData, setFormData] = useState({
    firstName: user?.first_name || '',
    lastName: user?.last_name || '',
    email: user?.email || '',
  })

  const [preferences, setPreferences] = useState({
    emailNotifications: true,
    pushNotifications: true,
    newsletterFrequency: 'daily',
    theme: theme,
    autoRefresh: true,
    refreshInterval: 30,
  })

  const handleSaveProfile = () => {
    // In a real app, this would call the API
    updateUser({
      first_name: formData.firstName,
      last_name: formData.lastName,
      email: formData.email,
    })

    addNotification({
      type: 'success',
      message: 'Profile updated successfully',
      duration: 3000,
    })
  }

  const handleSavePreferences = () => {
    setTheme(preferences.theme)

    addNotification({
      type: 'success',
      message: 'Preferences updated successfully',
      duration: 3000,
    })
  }

  const handleExportData = () => {
    // In a real app, this would trigger a data export
    addNotification({
      type: 'success',
      message: 'Data export initiated. You will receive an email when ready.',
      duration: 5000,
    })
  }

  const handleDeleteAccount = () => {
    // In a real app, this would show a confirmation dialog
    addNotification({
      type: 'error',
      message: 'Account deletion requires additional verification',
      duration: 5000,
    })
  }

  return (
    <div className="max-w-4xl mx-auto p-6 space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-foreground">Settings</h1>
        <p className="text-muted-foreground">
          Manage your account, preferences, and application settings
        </p>
      </div>

      {/* Profile Settings */}
      <div className="bg-card border border-border rounded-lg p-6">
        <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
          <Shield className="w-5 h-5" />
          Profile Information
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
          <div>
            <label className="block text-sm font-medium mb-2">First Name</label>
            <Input
              value={formData.firstName}
              onChange={(e) => setFormData(prev => ({ ...prev, firstName: e.target.value }))}
              placeholder="Enter your first name"
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">Last Name</label>
            <Input
              value={formData.lastName}
              onChange={(e) => setFormData(prev => ({ ...prev, lastName: e.target.value }))}
              placeholder="Enter your last name"
            />
          </div>

          <div className="md:col-span-2">
            <label className="block text-sm font-medium mb-2">Email Address</label>
            <Input
              type="email"
              value={formData.email}
              onChange={(e) => setFormData(prev => ({ ...prev, email: e.target.value }))}
              placeholder="Enter your email address"
            />
          </div>
        </div>

        <Button onClick={handleSaveProfile} className="flex items-center gap-2">
          <Save className="w-4 h-4" />
          Save Profile
        </Button>
      </div>

      {/* Notification Preferences */}
      <div className="bg-card border border-border rounded-lg p-6">
        <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
          <Bell className="w-5 h-5" />
          Notification Preferences
        </h2>

        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <label className="text-sm font-medium">Email Notifications</label>
              <p className="text-xs text-muted-foreground">Receive email updates about your research</p>
            </div>
            <input
              type="checkbox"
              checked={preferences.emailNotifications}
              onChange={(e) => setPreferences(prev => ({ ...prev, emailNotifications: e.target.checked }))}
              className="rounded border-border"
            />
          </div>

          <div className="flex items-center justify-between">
            <div>
              <label className="text-sm font-medium">Push Notifications</label>
              <p className="text-xs text-muted-foreground">Receive browser notifications for alerts</p>
            </div>
            <input
              type="checkbox"
              checked={preferences.pushNotifications}
              onChange={(e) => setPreferences(prev => ({ ...prev, pushNotifications: e.target.checked }))}
              className="rounded border-border"
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">Newsletter Frequency</label>
            <select
              value={preferences.newsletterFrequency}
              onChange={(e) => setPreferences(prev => ({ ...prev, newsletterFrequency: e.target.value }))}
              className="w-full md:w-48 px-3 py-2 border border-border rounded-md bg-background"
            >
              <option value="real-time">Real-time</option>
              <option value="hourly">Hourly</option>
              <option value="daily">Daily</option>
              <option value="weekly">Weekly</option>
              <option value="never">Never</option>
            </select>
          </div>
        </div>

        <Button onClick={handleSavePreferences} className="mt-6 flex items-center gap-2">
          <Save className="w-4 h-4" />
          Save Preferences
        </Button>
      </div>

      {/* Appearance Settings */}
      <div className="bg-card border border-border rounded-lg p-6">
        <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
          <Monitor className="w-5 h-5" />
          Appearance
        </h2>

        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-3">Theme</label>
            <div className="flex gap-3">
              {[
                { value: 'light', icon: Sun, label: 'Light' },
                { value: 'dark', icon: Moon, label: 'Dark' },
                { value: 'auto', icon: Monitor, label: 'Auto' },
              ].map(({ value, icon: Icon, label }) => (
                <button
                  key={value}
                  onClick={() => setPreferences(prev => ({ ...prev, theme: value as any }))}
                  className={`flex items-center gap-2 px-4 py-2 rounded-md border transition-colors ${
                    preferences.theme === value
                      ? 'border-primary bg-primary/10 text-primary'
                      : 'border-border hover:border-primary/50'
                  }`}
                >
                  <Icon className="w-4 h-4" />
                  <span className="text-sm">{label}</span>
                </button>
              ))}
            </div>
          </div>

          <div className="flex items-center justify-between">
            <div>
              <label className="text-sm font-medium">Auto-refresh Feed</label>
              <p className="text-xs text-muted-foreground">Automatically refresh content in the background</p>
            </div>
            <input
              type="checkbox"
              checked={preferences.autoRefresh}
              onChange={(e) => setPreferences(prev => ({ ...prev, autoRefresh: e.target.checked }))}
              className="rounded border-border"
            />
          </div>

          {preferences.autoRefresh && (
            <div>
              <label className="block text-sm font-medium mb-2">Refresh Interval (seconds)</label>
              <Input
                type="number"
                value={preferences.refreshInterval}
                onChange={(e) => setPreferences(prev => ({
                  ...prev,
                  refreshInterval: parseInt(e.target.value) || 30
                }))}
                min="10"
                max="300"
                className="w-32"
              />
            </div>
          )}
        </div>
      </div>

      {/* Data Management */}
      <div className="bg-card border border-border rounded-lg p-6">
        <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
          <Download className="w-5 h-5" />
          Data Management
        </h2>

        <div className="space-y-4">
          <div className="flex items-center justify-between p-4 bg-muted/50 rounded-lg">
            <div>
              <h3 className="font-medium">Export Your Data</h3>
              <p className="text-sm text-muted-foreground">
                Download all your research items, saved content, and preferences
              </p>
            </div>
            <Button variant="outline" onClick={handleExportData}>
              <Download className="w-4 h-4 mr-2" />
              Export Data
            </Button>
          </div>

          <div className="flex items-center justify-between p-4 bg-destructive/10 border border-destructive/20 rounded-lg">
            <div>
              <h3 className="font-medium text-destructive">Danger Zone</h3>
              <p className="text-sm text-muted-foreground">
                Permanently delete your account and all associated data
              </p>
            </div>
            <Button variant="destructive" onClick={handleDeleteAccount}>
              <Trash2 className="w-4 h-4 mr-2" />
              Delete Account
            </Button>
          </div>
        </div>
      </div>

      {/* Footer */}
      <div className="text-center text-sm text-muted-foreground">
        <p>Knowledge Graph Lab v1.0.0</p>
        <p>Built with React, TypeScript, and Tailwind CSS</p>
      </div>
    </div>
  )
}