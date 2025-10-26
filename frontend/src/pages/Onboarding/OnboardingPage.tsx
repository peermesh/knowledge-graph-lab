import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { ArrowRight, CheckCircle } from 'lucide-react'

import { Button } from '@/components/Common/Button'
import { BubbleInterface } from '@/components/Onboarding/BubbleInterface'
import { useUserStore } from '@/store/useUserStore'

export function OnboardingPage() {
  const navigate = useNavigate()
  const { login } = useUserStore()
  const [currentStep, setCurrentStep] = useState(0)
  const [interests, setInterests] = useState<string[]>([])

  const steps = [
    {
      title: 'Welcome to Knowledge Graph Lab',
      description: 'Transform information chaos into actionable intelligence',
      content: (
        <div className="text-center">
          <div className="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-4">
            <span className="text-2xl">🎯</span>
          </div>
          <p className="text-muted-foreground">
            Let's personalize your experience by learning about your interests.
          </p>
        </div>
      ),
    },
    {
      title: 'Explore Your Interests',
      description: 'Use our interactive bubble interface to discover relevant topics',
      content: <BubbleInterface onInterestsChange={setInterests} />,
    },
    {
      title: 'Setup Complete!',
      description: 'Your personalized research feed is ready',
      content: (
        <div className="text-center">
          <CheckCircle className="w-16 h-16 text-green-500 mx-auto mb-4" />
          <p className="text-muted-foreground mb-4">
            We've configured your personalized research feed based on your interests.
          </p>
          <div className="bg-muted p-4 rounded-lg text-left">
            <h4 className="font-medium mb-2">Selected Interests:</h4>
            <div className="flex flex-wrap gap-2">
              {interests.slice(0, 5).map((interest) => (
                <span
                  key={interest}
                  className="px-2 py-1 bg-primary/10 text-primary rounded text-sm"
                >
                  {interest}
                </span>
              ))}
              {interests.length > 5 && (
                <span className="px-2 py-1 bg-muted text-muted-foreground rounded text-sm">
                  +{interests.length - 5} more
                </span>
              )}
            </div>
          </div>
        </div>
      ),
    },
  ]

  const handleNext = () => {
    if (currentStep < steps.length - 1) {
      setCurrentStep(currentStep + 1)
    } else {
      // Complete onboarding
      handleComplete()
    }
  }

  const handleComplete = () => {
    // Save interests to user profile
    login({
      id: 'user-1',
      email: 'user@example.com',
      first_name: 'Research',
      last_name: 'User',
      role: 'user',
      is_active: true,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    }, 'mock-token', 'mock-refresh')

    // Navigate to feed
    navigate('/feed')
  }

  const canProceed = () => {
    if (currentStep === 0) return true
    if (currentStep === 1) return interests.length > 0
    return true
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary/5 to-secondary/5 flex items-center justify-center p-4">
      <div className="max-w-2xl w-full bg-card rounded-lg shadow-lg p-8">
        {/* Progress indicator */}
        <div className="flex items-center justify-center mb-8">
          {steps.map((_, index) => (
            <React.Fragment key={index}>
              <div
                className={`w-3 h-3 rounded-full ${
                  index <= currentStep
                    ? 'bg-primary'
                    : 'bg-muted'
                }`}
              />
              {index < steps.length - 1 && (
                <div
                  className={`w-12 h-0.5 mx-2 ${
                    index < currentStep
                      ? 'bg-primary'
                      : 'bg-muted'
                  }`}
                />
              )}
            </React.Fragment>
          ))}
        </div>

        {/* Step content */}
        <div className="mb-8">
          <h1 className="text-2xl font-bold text-center mb-2">
            {steps[currentStep].title}
          </h1>
          <p className="text-muted-foreground text-center mb-6">
            {steps[currentStep].description}
          </p>

          <div className="min-h-64">
            {steps[currentStep].content}
          </div>
        </div>

        {/* Navigation */}
        <div className="flex justify-between">
          <Button
            variant="outline"
            onClick={() => setCurrentStep(Math.max(0, currentStep - 1))}
            disabled={currentStep === 0}
          >
            Previous
          </Button>

          <Button
            onClick={handleNext}
            disabled={!canProceed()}
            className="flex items-center gap-2"
          >
            {currentStep === steps.length - 1 ? 'Get Started' : 'Next'}
            <ArrowRight className="w-4 h-4" />
          </Button>
        </div>
      </div>
    </div>
  )
}