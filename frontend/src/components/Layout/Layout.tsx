import { Outlet } from 'react-router-dom'

import { ThreePanelLayout } from './ThreePanelLayout'

interface LayoutProps {
  className?: string
}

export function Layout({ className = '' }: LayoutProps) {
  return (
    <div className={`min-h-screen bg-background ${className}`}>
      <ThreePanelLayout>
        <Outlet />
      </ThreePanelLayout>
    </div>
  )
}
