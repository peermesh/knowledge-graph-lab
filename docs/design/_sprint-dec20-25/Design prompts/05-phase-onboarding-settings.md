# Phase 5: Onboarding & Settings

## Objective

Build the first-time user onboarding flow and the settings interface. These complete the core user journey.

## What to Build

### 1. Onboarding Flow

A 3-4 screen sequence for new users.

**OnboardingWelcome.tsx**
First screen.
- App logo/name
- Welcoming headline: "Stay informed about what matters"
- Brief value prop (1-2 sentences)
- "Get Started" button

**OnboardingFirstTopic.tsx**
Second screen - create first research interest.
- Headline: "What would you like to stay informed about?"
- Large text input field
- Example placeholders cycling: "Tesla's manufacturing strategy", "AI regulation updates", "My competitor's announcements"
- "Continue" button (disabled until input)

**OnboardingFrequency.tsx**
Third screen - set update preference.
- Headline: "How often do you want updates?"
- Three options as large tappable cards:
  - "Daily" - Brief daily digest
  - "Weekly" - Comprehensive weekly summary
  - "Real-time" - As discoveries happen
- Selected state clearly indicated

**OnboardingDelivery.tsx**
Fourth screen - choose delivery method.
- Headline: "Where should we send your findings?"
- Options as toggles:
  - "In this app" (always on, not toggleable)
  - "Email" - reveals email input when toggled
  - "Phone notifications" - reveals phone input when toggled
- "Finish Setup" button

**OnboardingComplete.tsx**
Final screen.
- Success message: "You're all set!"
- Shows summary: "We'll research [topic] and send [frequency] updates to [destinations]"
- "Start Exploring" button → redirects to Discover mode

### 2. Onboarding State

Track onboarding progress:
```typescript
interface OnboardingState {
  currentStep: number;
  firstTopic: string;
  frequency: 'daily' | 'weekly' | 'realtime';
  deliveryMethods: {
    email: string | null;
    phone: string | null;
  };
}
```

Persist to localStorage so refresh doesn't lose progress.

### 3. Settings Interface

**SettingsPanel.tsx**
Slide-out panel from right side (desktop) or full-screen (mobile).

Sections:

**Account Section**
- Profile photo placeholder
- Name (editable)
- Email (display only)
- "Sign Out" button

**Preferences Section**
- Default update frequency (dropdown)
- Time zone (dropdown)
- Notification preferences (toggles)

**Publishing Defaults Section**
- Default trust level for new streams (Auto/Review)
- Default destinations for new streams (checkboxes)

**Data Section**
- "Export my data" button (mock)
- "Delete account" button (mock, with confirmation)

**About Section**
- App version
- Links: Help, Privacy Policy, Terms of Service (can be # hrefs)

### 4. Settings Components

**SettingsSection.tsx**
Wrapper for a settings group.
- Section title
- Children (form elements)
- Divider below

**SettingsToggle.tsx**
Toggle switch with label.

**SettingsSelect.tsx**
Dropdown selector with label.

**SettingsInput.tsx**
Text input with label.

**SettingsButton.tsx**
Action button (for export, delete, sign out).

### 5. Settings Trigger

Update the navigation:
- Profile/settings icon in nav
- Clicking opens SettingsPanel
- Panel has close button
- Clicking outside closes panel (desktop)

### 6. Mock Data

```typescript
// src/fixtures/user.ts
export const mockUser = {
  name: 'Alex Chen',
  email: 'alex@example.com',
  photoUrl: null,
  preferences: {
    defaultFrequency: 'daily',
    timezone: 'America/Los_Angeles',
    notifications: {
      email: true,
      push: true,
      sms: false,
    }
  },
  publishingDefaults: {
    trustLevel: 'review',
    destinations: ['email'],
  }
};
```

## Acceptance Criteria

### Onboarding
- [ ] Welcome screen displays correctly
- [ ] Can enter first research topic
- [ ] Can select update frequency
- [ ] Can toggle delivery methods and enter contact info
- [ ] Completion screen shows summary
- [ ] Finishing redirects to Discover mode
- [ ] Progress persists across refresh
- [ ] Can navigate back to previous steps

### Settings
- [ ] Settings panel opens from nav icon
- [ ] Panel slides in smoothly
- [ ] All sections display correctly
- [ ] Toggles and inputs are interactive
- [ ] Changes persist (localStorage is fine)
- [ ] Sign out clears auth state
- [ ] Panel closes when clicking outside (desktop)
- [ ] Close button works
- [ ] Mobile layout works (full screen)

## Design Notes

### Onboarding
- Should feel welcoming and low-friction
- One question per screen, no overwhelm
- Clear progress indication (dots or steps)
- Skip option is okay but not prominent
- Celebrate completion

### Settings
- Organized into clear sections
- Easy to scan and find things
- Destructive actions need confirmation
- Keep it simple - avoid nested settings

## Do NOT Build Yet

- Real authentication
- Real data export
- Account deletion logic
- OAuth integrations
- Profile photo upload
