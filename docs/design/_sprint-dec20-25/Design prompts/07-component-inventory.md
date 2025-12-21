# Component Inventory

A reference of all components to be built, organized by category.

## Layout Components

| Component | Phase | Description |
|-----------|-------|-------------|
| AppShell | 1 | Main wrapper with nav and content area |
| DesktopNav | 1 | Left rail navigation for desktop |
| MobileNav | 1 | Bottom tab bar for mobile |
| SettingsPanel | 5 | Slide-out settings interface |

## Discover Mode Components

| Component | Phase | Description |
|-----------|-------|-------------|
| FeedList | 2 | Virtualized list of findings |
| FindingCard | 2 | Individual finding display |
| SuggestionCard | 2 | Topic suggestion prompt |
| DomainSelector | 2 | Overlay for assigning domains |

## Organize Mode Components

| Component | Phase | Description |
|-----------|-------|-------------|
| DomainTree | 3 | Main tree view container |
| DomainNode | 3 | Single tree node |
| DomainContextMenu | 3 | Right-click/long-press menu |
| AddDomainInput | 3 | Inline input for new domains |
| MoveDomainDialog | 3 | Modal for moving domains |
| DomainDetail | 3 | Selected domain detail panel |

## Publish Mode Components

| Component | Phase | Description |
|-----------|-------|-------------|
| PublishQueue | 4 | Container for pending items |
| PublicationCard | 4 | Pending publication display |
| EmptyQueueState | 4 | Shown when queue empty |
| DestinationsList | 4 | List of publishing destinations |
| DestinationRow | 4 | Single destination entry |
| AddDestinationFlow | 4 | Flow for adding destinations |
| DomainPublishSettings | 4 | Per-domain publish config |

## Onboarding Components

| Component | Phase | Description |
|-----------|-------|-------------|
| OnboardingWelcome | 5 | Welcome screen |
| OnboardingFirstTopic | 5 | First topic input |
| OnboardingFrequency | 5 | Frequency selection |
| OnboardingDelivery | 5 | Delivery method setup |
| OnboardingComplete | 5 | Completion confirmation |

## Settings Components

| Component | Phase | Description |
|-----------|-------|-------------|
| SettingsSection | 5 | Section wrapper |
| SettingsToggle | 5 | Toggle switch with label |
| SettingsSelect | 5 | Dropdown with label |
| SettingsInput | 5 | Text input with label |
| SettingsButton | 5 | Action button |

## Shared Components

| Component | Phase | Description |
|-----------|-------|-------------|
| Toast | 6 | Notification toast |
| ConfirmDialog | 6 | Confirmation modal |
| LoadingCard | 6 | Skeleton loading state |
| EmptyState | 6 | Generic empty state |
| Badge | 1 | Notification count badge |
| IconButton | 1 | Button with icon only |

## Data Types

```typescript
interface Finding {
  id: string;
  title: string;
  summary: string;
  source: string;
  timestamp: Date;
  domain: string;
  imageUrl?: string;
}

interface Suggestion {
  prompt: string;
  suggestions: Array<{
    id: string;
    label: string;
    description: string;
  }>;
}

interface DomainNode {
  id: string;
  name: string;
  findingCount: number;
  children: DomainNode[];
}

interface PendingPublication {
  id: string;
  content: string;
  destination: string;
  scheduledTime: Date;
  sourceFinding: {
    title: string;
    domain: string;
  };
}

interface Destination {
  id: string;
  type: 'email' | 'phone' | 'twitter' | 'linkedin';
  identifier: string;
  enabled: boolean;
  status: 'connected' | 'error' | 'pending';
}

interface User {
  name: string;
  email: string;
  photoUrl: string | null;
  preferences: Preferences;
}

interface Preferences {
  defaultFrequency: 'daily' | 'weekly' | 'realtime';
  timezone: string;
  notifications: {
    email: boolean;
    push: boolean;
    sms: boolean;
  };
  publishingDefaults: {
    trustLevel: 'auto' | 'review';
    destinations: string[];
  };
}
```

## File Structure

```
src/
├── components/
│   ├── layout/
│   │   ├── AppShell.tsx
│   │   ├── DesktopNav.tsx
│   │   ├── MobileNav.tsx
│   │   └── SettingsPanel.tsx
│   ├── discover/
│   │   ├── FeedList.tsx
│   │   ├── FindingCard.tsx
│   │   ├── SuggestionCard.tsx
│   │   └── DomainSelector.tsx
│   ├── organize/
│   │   ├── DomainTree.tsx
│   │   ├── DomainNode.tsx
│   │   ├── DomainContextMenu.tsx
│   │   ├── AddDomainInput.tsx
│   │   ├── MoveDomainDialog.tsx
│   │   └── DomainDetail.tsx
│   ├── publish/
│   │   ├── PublishQueue.tsx
│   │   ├── PublicationCard.tsx
│   │   ├── EmptyQueueState.tsx
│   │   ├── DestinationsList.tsx
│   │   ├── DestinationRow.tsx
│   │   ├── AddDestinationFlow.tsx
│   │   └── DomainPublishSettings.tsx
│   ├── onboarding/
│   │   ├── OnboardingWelcome.tsx
│   │   ├── OnboardingFirstTopic.tsx
│   │   ├── OnboardingFrequency.tsx
│   │   ├── OnboardingDelivery.tsx
│   │   └── OnboardingComplete.tsx
│   ├── settings/
│   │   ├── SettingsSection.tsx
│   │   ├── SettingsToggle.tsx
│   │   ├── SettingsSelect.tsx
│   │   ├── SettingsInput.tsx
│   │   └── SettingsButton.tsx
│   └── shared/
│       ├── Toast.tsx
│       ├── ConfirmDialog.tsx
│       ├── LoadingCard.tsx
│       ├── EmptyState.tsx
│       ├── Badge.tsx
│       └── IconButton.tsx
├── pages/
│   ├── DiscoverPage.tsx
│   ├── OrganizePage.tsx
│   ├── PublishPage.tsx
│   └── OnboardingPage.tsx
├── hooks/
│   ├── useAuth.ts
│   ├── useDomains.ts
│   ├── useFindings.ts
│   ├── usePublishing.ts
│   └── useSettings.ts
├── context/
│   ├── AuthContext.tsx
│   └── AppStateContext.tsx
├── fixtures/
│   ├── findings.ts
│   ├── domains.ts
│   ├── publishing.ts
│   └── user.ts
├── types/
│   └── index.ts
└── utils/
    └── storage.ts
```
