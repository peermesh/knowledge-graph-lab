import { Routes, Route, Navigate } from 'react-router-dom'

import { ThreePanelLayout } from '@/components/Layout/ThreePanelLayout'
import { FeedPage } from '@/pages/Feed/FeedPage'
import { GraphLabPage } from '@/pages/Lab/GraphLabPage'
import { SettingsPage } from '@/pages/Settings/SettingsPage'

function App() {
  return (
    <ThreePanelLayout>
      <Routes>
        <Route path="/" element={<Navigate to="/feed" replace />} />
        <Route path="/feed" element={<FeedPage />} />
        <Route path="/lab" element={<GraphLabPage />} />
        <Route path="/settings" element={<SettingsPage />} />
        <Route path="*" element={<div className="p-6"><h1>404 - Page Not Found</h1></div>} />
      </Routes>
    </ThreePanelLayout>
  )
}

export default App