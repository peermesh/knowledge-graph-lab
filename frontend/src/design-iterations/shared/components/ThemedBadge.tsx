import React from 'react'
import { useDesignTheme } from '../ThemeProvider'

interface ThemedBadgeProps {
  children: React.ReactNode
  variant?: 'primary' | 'accent' | 'secondary' | 'success' | 'warning' | 'error' | 'neutral'
  size?: 'sm' | 'md'
  icon?: React.ReactNode
  onClick?: () => void
}

export function ThemedBadge({ children, variant = 'primary', size = 'sm', icon, onClick }: ThemedBadgeProps) {
  const theme = useDesignTheme()
  const [isHovered, setIsHovered] = React.useState(false)

  const getColors = () => {
    const variants = {
      primary: { bg: theme.colors.primary[100], text: theme.colors.primary[700], hoverBg: theme.colors.primary[200] },
      accent: { bg: theme.colors.accent[100], text: theme.colors.accent[700], hoverBg: theme.colors.accent[200] },
      secondary: { bg: theme.colors.secondary[100], text: theme.colors.secondary[700], hoverBg: theme.colors.secondary[200] },
      success: { bg: '#D1FAE5', text: '#065F46', hoverBg: '#A7F3D0' },
      warning: { bg: '#FEF3C7', text: '#92400E', hoverBg: '#FDE68A' },
      error: { bg: '#FEE2E2', text: '#991B1B', hoverBg: '#FECACA' },
      neutral: { bg: theme.colors.neutral[100], text: theme.colors.neutral[700], hoverBg: theme.colors.neutral[200] },
    }
    return variants[variant]
  }

  const colors = getColors()

  const styles: React.CSSProperties = {
    display: 'inline-flex',
    alignItems: 'center',
    gap: '0.375rem',
    padding: size === 'sm' ? '0.375rem 0.75rem' : '0.5rem 1rem',
    borderRadius: theme.borderRadius.sm,
    fontSize: size === 'sm' ? theme.typography.fontSize.xs : theme.typography.fontSize.sm,
    fontWeight: theme.typography.fontWeight.medium,
    background: isHovered && onClick ? colors.hoverBg : colors.bg,
    color: colors.text,
    cursor: onClick ? 'pointer' : 'default',
    transition: 'all 150ms ease',
    whiteSpace: 'nowrap',
  }

  return (
    <span
      style={styles}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
      onClick={onClick}
    >
      {icon}
      {children}
    </span>
  )
}

