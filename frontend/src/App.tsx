import { Routes, Route, Navigate } from 'react-router-dom'

import { ThreePanelLayout } from '@/components/Layout/ThreePanelLayout'
import { FeedPage } from '@/pages/Feed/FeedPage'
import { GraphLabPage } from '@/pages/Lab/GraphLabPage'
import { SettingsPage } from '@/pages/Settings/SettingsPage'
import { AddTopicsPage } from '@/pages/AddTopics/AddTopicsPage'
import { OnboardingPage } from '@/pages/Onboarding/OnboardingPage'

// Design Iterations
import { DesignShowcase } from '@/design-iterations/showcase/DesignShowcase'
import { FeedPageV1 } from '@/design-iterations/iteration-1/pages/FeedPageV1'
import { GraphLabPageV1 } from '@/design-iterations/iteration-1/pages/GraphLabPageV1'
import { SettingsPageV1 } from '@/design-iterations/iteration-1/pages/SettingsPageV1'
import { FeedPageV2 } from '@/design-iterations/iteration-2/pages/FeedPageV2'
import { GraphLabPageV2 } from '@/design-iterations/iteration-2/pages/GraphLabPageV2'
import { SettingsPageV2 } from '@/design-iterations/iteration-2/pages/SettingsPageV2'
import { FeedPageV3 } from '@/design-iterations/iteration-3/pages/FeedPageV3'
import { GraphLabPageV3 } from '@/design-iterations/iteration-3/pages/GraphLabPageV3'
import { SettingsPageV3 } from '@/design-iterations/iteration-3/pages/SettingsPageV3'

function App() {
  return (
    <Routes>
      {/* Design Showcase - outside of ThreePanelLayout */}
      <Route path="/design-showcase" element={<DesignShowcase />} />
      
      {/* Iteration 1 Routes - outside of ThreePanelLayout */}
      <Route path="/iterations/v1/feed" element={<FeedPageV1 />} />
      <Route path="/iterations/v1/lab" element={<GraphLabPageV1 />} />
      <Route path="/iterations/v1/settings" element={<SettingsPageV1 />} />
      
      {/* Iteration 2 Routes - outside of ThreePanelLayout */}
      <Route path="/iterations/v2/feed" element={<FeedPageV2 />} />
      <Route path="/iterations/v2/lab" element={<GraphLabPageV2 />} />
      <Route path="/iterations/v2/settings" element={<SettingsPageV2 />} />
      
      {/* Iteration 3 Routes - outside of ThreePanelLayout */}
      <Route path="/iterations/v3/feed" element={<FeedPageV3 />} />
      <Route path="/iterations/v3/lab" element={<GraphLabPageV3 />} />
      <Route path="/iterations/v3/settings" element={<SettingsPageV3 />} />
      
      {/* Original Routes - inside ThreePanelLayout */}
      <Route path="/*" element={
        <ThreePanelLayout>
          <Routes>
            <Route path="/" element={<Navigate to="/feed" replace />} />
            <Route path="/feed" element={<FeedPage />} />
            <Route path="/lab" element={<GraphLabPage />} />
            <Route path="/settings" element={<SettingsPage />} />
            <Route path="/onboarding" element={<OnboardingPage />} />
            <Route path="/add-topics" element={<AddTopicsPage mode="add" />} />
            <Route path="*" element={<div className="p-6"><h1>404 - Page Not Found</h1></div>} />
          </Routes>
        </ThreePanelLayout>
      } />
    </Routes>
  )
}

export default App