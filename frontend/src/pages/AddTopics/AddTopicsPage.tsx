import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { ArrowLeft, Check, X } from 'lucide-react'

import { Button } from '@/components/Common/Button'
import { BubbleInterface } from '@/components/Onboarding/BubbleInterface'
import { useUserStore } from '@/store/useUserStore'
import { useUIStore } from '@/store/useUIStore'

interface AddTopicsPageProps {
  mode?: 'onboarding' | 'add'
}

export function AddTopicsPage({ mode = 'add' }: AddTopicsPageProps) {
  const navigate = useNavigate()
  const { user } = useUserStore()
  const { addNotification } = useUIStore()
  const [selectedInterests, setSelectedInterests] = useState<string[]>([])

  const isOnboarding = mode === 'onboarding' || !user

  const handleSave = async () => {
    if (selectedInterests.length === 0) {
      addNotification({
        type: 'error',
        message: 'Please select at least one topic to continue',
        duration: 3000,
      })
      return
    }

    // TODO: Save interests to backend API
    // POST /api/user/interests
    // { interests: selectedInterests }

    addNotification({
      type: 'success',
      message: `${selectedInterests.length} topic${selectedInterests.length > 1 ? 's' : ''} added to your feed`,
      duration: 3000,
    })

    // Navigate back to feed
    navigate('/feed')
  }

  const handleCancel = () => {
    if (isOnboarding) {
      // For new users, maybe show a warning or skip for now
      addNotification({
        type: 'info',
        message: 'You can add topics anytime from the feed page',
        duration: 3000,
      })
    }
    navigate('/feed')
  }

  return (
    <div className="h-full flex flex-col bg-background">
      {/* Header */}
      <div className="border-b border-border p-6">
        <div className="max-w-4xl mx-auto">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-3">
              {!isOnboarding && (
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={handleCancel}
                  className="mr-2"
                >
                  <ArrowLeft className="w-4 h-4" />
                </Button>
              )}
              <div>
                <h1 className="text-2xl font-bold text-foreground">
                  {isOnboarding ? 'Welcome! Discover Your Interests' : 'Add Research Topics'}
                </h1>
                <p className="text-muted-foreground mt-1">
                  {isOnboarding
                    ? 'Select topics you want to explore and stay updated on'
                    : 'Expand your research feed with new topics'}
                </p>
              </div>
            </div>

            <div className="flex items-center gap-2">
              {!isOnboarding && (
                <Button variant="outline" onClick={handleCancel}>
                  <X className="w-4 h-4 mr-2" />
                  Cancel
                </Button>
              )}
              <Button
                onClick={handleSave}
                disabled={selectedInterests.length === 0}
              >
                <Check className="w-4 h-4 mr-2" />
                {isOnboarding ? 'Continue' : 'Save Topics'}
              </Button>
            </div>
          </div>

          {/* Instructions */}
          <div className="bg-primary/5 border border-primary/20 rounded-lg p-4">
            <h3 className="text-sm font-semibold text-primary mb-2">How it works:</h3>
            <ul className="text-sm text-muted-foreground space-y-1">
              <li className="flex items-start gap-2">
                <span className="text-primary font-bold">1.</span>
                <span>Enter a topic you're interested in below</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-primary font-bold">2.</span>
                <span>Click the <span className="inline-flex items-center justify-center w-4 h-4 bg-green-500 rounded-full text-white text-xs">✓</span> to add topics you like</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-primary font-bold">3.</span>
                <span>Click the <span className="inline-flex items-center justify-center w-4 h-4 bg-red-500 rounded-full text-white text-xs">×</span> to hide topics you're not interested in</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-primary font-bold">4.</span>
                <span>Click on a topic bubble to explore related sub-topics</span>
              </li>
            </ul>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 overflow-auto p-6">
        <div className="max-w-4xl mx-auto">
          <BubbleInterface
            onInterestsChange={setSelectedInterests}
            className="min-h-[600px]"
          />

          {/* Selected Count */}
          {selectedInterests.length > 0 && (
            <div className="mt-6 text-center">
              <p className="text-muted-foreground">
                <span className="font-semibold text-foreground">{selectedInterests.length}</span> topic
                {selectedInterests.length > 1 ? 's' : ''} selected
              </p>
            </div>
          )}
        </div>
      </div>

      {/* Footer Actions (Mobile) */}
      <div className="border-t border-border p-4 bg-card md:hidden">
        <div className="flex gap-2">
          {!isOnboarding && (
            <Button variant="outline" onClick={handleCancel} className="flex-1">
              Cancel
            </Button>
          )}
          <Button
            onClick={handleSave}
            disabled={selectedInterests.length === 0}
            className="flex-1"
          >
            {isOnboarding ? 'Continue' : 'Save Topics'}
          </Button>
        </div>
      </div>
    </div>
  )
}

