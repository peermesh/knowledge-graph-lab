import React, { useState, useRef, useEffect } from 'react'
import { cn } from '@/utils/cn'

interface ResizablePanelProps {
  children: React.ReactNode
  defaultWidth?: number
  minWidth?: number
  maxWidth?: number
  collapsed?: boolean
  onCollapsedChange?: (collapsed: boolean) => void
  side: 'left' | 'right'
  className?: string
}

export function ResizablePanel({
  children,
  defaultWidth = 280,
  minWidth = 200,
  maxWidth = 500,
  collapsed = false,
  side,
  className,
}: ResizablePanelProps) {
  const [width, setWidth] = useState(defaultWidth)
  const [isResizing, setIsResizing] = useState(false)
  const panelRef = useRef<HTMLDivElement>(null)
  const resizeHandleRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (collapsed) {
      setWidth(0)
    } else {
      setWidth(defaultWidth)
    }
  }, [collapsed, defaultWidth])

  const handleMouseDown = (e: React.MouseEvent) => {
    setIsResizing(true)
    e.preventDefault()
  }

  const handleMouseMove = (e: MouseEvent) => {
    if (!isResizing || !panelRef.current) return

    const rect = panelRef.current.getBoundingClientRect()
    let newWidth

    if (side === 'left') {
      newWidth = e.clientX - rect.left
    } else {
      newWidth = rect.right - e.clientX
    }

    // Constrain width
    newWidth = Math.max(minWidth, Math.min(maxWidth, newWidth))
    setWidth(newWidth)
  }

  const handleMouseUp = () => {
    setIsResizing(false)
  }

  useEffect(() => {
    if (isResizing) {
      document.addEventListener('mousemove', handleMouseMove)
      document.addEventListener('mouseup', handleMouseUp)
      document.body.style.cursor = 'col-resize'
      document.body.style.userSelect = 'none'

      return () => {
        document.removeEventListener('mousemove', handleMouseMove)
        document.removeEventListener('mouseup', handleMouseUp)
        document.body.style.cursor = ''
        document.body.style.userSelect = ''
      }
    }
  }, [isResizing, side])

  if (collapsed) {
    return null
  }

  return (
    <div
      ref={panelRef}
      className={cn(
        'relative flex-shrink-0 bg-background border-r border-border',
        className
      )}
      style={{ width: `${width}px` }}
    >
      {/* Panel Content */}
      <div className="h-full overflow-hidden">
        {children}
      </div>

      {/* Resize Handle */}
      <div
        ref={resizeHandleRef}
        className={cn(
          'absolute top-0 h-full w-1 bg-border hover:bg-ring cursor-col-resize transition-colors',
          side === 'left' ? 'right-0' : 'left-0'
        )}
        onMouseDown={handleMouseDown}
        style={{
          [side === 'left' ? 'right' : 'left']: '-2px',
        }}
      />

      {/* Resize Handle Visual Feedback */}
      {isResizing && (
        <div
          className={cn(
            'absolute top-0 h-full w-0.5 bg-ring z-10',
            side === 'left' ? 'right-0' : 'left-0'
          )}
        />
      )}
    </div>
  )
}
