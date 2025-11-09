import React from 'react'
import { useDesignTheme } from '../ThemeProvider'

interface ThemedCardProps {
  children: React.ReactNode
  className?: string
  accentBorder?: 'left' | 'top' | 'none'
  onClick?: () => void
}

export function ThemedCard({ children, className = '', accentBorder = 'left', onClick }: ThemedCardProps) {
  const theme = useDesignTheme()
  const [isHovered, setIsHovered] = React.useState(false)

  const styles: React.CSSProperties = {
    background: 'white',
    borderRadius: theme.borderRadius.lg,
    padding: theme.spacing.lg,
    border: `1px solid ${theme.colors.neutral[200]}`,
    boxShadow: isHovered ? theme.shadows.lg : theme.shadows.md,
    transition: 'all 300ms cubic-bezier(0.4, 0, 0.2, 1)',
    cursor: onClick ? 'pointer' : 'default',
    transform: isHovered && onClick ? 'translateY(-2px)' : 'translateY(0)',
    ...(accentBorder === 'left' && {
      borderLeft: `4px solid ${theme.colors.accent[500]}`,
    }),
    ...(accentBorder === 'top' && {
      borderTop: `3px solid ${theme.colors.accent[500]}`,
    }),
  }

  return (
    <div
      className={className}
      style={styles}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
      onClick={onClick}
    >
      {children}
    </div>
  )
}












