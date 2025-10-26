import { useState } from 'react'

import { MainNavigation } from '../Navigation/MainNavigation'
import { ResizablePanel } from './ResizablePanel'

interface ThreePanelLayoutProps {
  children?: React.ReactNode
  className?: string
}

export function ThreePanelLayout({ children, className = '' }: ThreePanelLayoutProps) {
  const [leftPanelCollapsed, setLeftPanelCollapsed] = useState(false)
  const [rightPanelVisible, setRightPanelVisible] = useState(true)

  return (
    <div className={`h-screen flex bg-background ${className}`}>
      {/* Left Panel - Navigation */}
      <ResizablePanel
        defaultWidth={280}
        minWidth={200}
        maxWidth={400}
        collapsed={leftPanelCollapsed}
        onCollapsedChange={setLeftPanelCollapsed}
        side="left"
        className="border-r border-border bg-card"
      >
        <MainNavigation />
      </ResizablePanel>

      {/* Center Panel - Main Content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        <main id="main-content" className="flex-1 overflow-auto">
          {children}
        </main>
      </div>

      {/* Right Panel - Context/Details */}
      {rightPanelVisible && (
        <ResizablePanel
          defaultWidth={320}
          minWidth={200}
          maxWidth={500}
          collapsed={!rightPanelVisible}
          onCollapsedChange={(collapsed) => setRightPanelVisible(!collapsed)}
          side="right"
          className="border-l border-border bg-card"
        >
          <div className="p-4">
            <h3 className="text-lg font-semibold mb-4">Context Panel</h3>
            <p className="text-muted-foreground">
              This panel will show contextual information based on the current view.
            </p>
          </div>
        </ResizablePanel>
      )}

      {/* Panel Toggle Buttons */}
      <div className="fixed top-4 right-4 z-50 flex gap-2">
        <button
          onClick={() => setLeftPanelCollapsed(!leftPanelCollapsed)}
          className="p-2 bg-primary text-primary-foreground rounded-md hover:bg-primary/90 transition-colors"
          aria-label={leftPanelCollapsed ? 'Expand navigation' : 'Collapse navigation'}
        >
          {leftPanelCollapsed ? '→' : '←'}
        </button>
        <button
          onClick={() => setRightPanelVisible(!rightPanelVisible)}
          className="p-2 bg-primary text-primary-foreground rounded-md hover:bg-primary/90 transition-colors"
          aria-label={rightPanelVisible ? 'Hide context panel' : 'Show context panel'}
        >
          {rightPanelVisible ? '→' : '←'}
        </button>
      </div>
    </div>
  )
}