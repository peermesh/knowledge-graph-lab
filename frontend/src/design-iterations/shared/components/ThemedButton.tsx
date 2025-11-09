import React from 'react'
import { useDesignTheme } from '../ThemeProvider'

interface ThemedButtonProps {
  children: React.ReactNode
  variant?: 'primary' | 'secondary' | 'ghost' | 'outline'
  size?: 'sm' | 'md' | 'lg'
  onClick?: () => void
  className?: string
  disabled?: boolean
  type?: 'button' | 'submit' | 'reset'
  icon?: React.ReactNode
}

export function ThemedButton({
  children,
  variant = 'primary',
  size = 'md',
  onClick,
  className = '',
  disabled = false,
  type = 'button',
  icon,
}: ThemedButtonProps) {
  const theme = useDesignTheme()
  const [isHovered, setIsHovered] = React.useState(false)

  const getStyles = () => {
    const baseStyles: React.CSSProperties = {
      display: 'inline-flex',
      alignItems: 'center',
      gap: '0.5rem',
      fontWeight: theme.typography.fontWeight.semibold,
      borderRadius: theme.borderRadius.md,
      transition: 'all 200ms ease',
      cursor: disabled ? 'not-allowed' : 'pointer',
      opacity: disabled ? 0.6 : 1,
      border: 'none',
    }

    const sizeStyles = {
      sm: { padding: '0.5rem 1rem', fontSize: theme.typography.fontSize.sm },
      md: { padding: '0.625rem 1.5rem', fontSize: theme.typography.fontSize.base },
      lg: { padding: '0.75rem 2rem', fontSize: theme.typography.fontSize.lg },
    }

    const variantStyles = {
      primary: {
        background: isHovered
          ? `linear-gradient(135deg, ${theme.colors.primary[600]} 0%, ${theme.colors.primary[700]} 100%)`
          : `linear-gradient(135deg, ${theme.colors.primary[500]} 0%, ${theme.colors.primary[600]} 100%)`,
        color: 'white',
        boxShadow: isHovered ? theme.shadows.lg : theme.shadows.md,
        transform: isHovered ? 'translateY(-1px)' : 'translateY(0)',
      },
      secondary: {
        background: isHovered ? theme.colors.neutral[200] : theme.colors.neutral[100],
        color: theme.colors.neutral[900],
        boxShadow: isHovered ? theme.shadows.md : theme.shadows.sm,
      },
      ghost: {
        background: isHovered ? theme.colors.neutral[100] : 'transparent',
        color: theme.colors.neutral[700],
      },
      outline: {
        background: 'white',
        color: theme.colors.primary[500],
        border: `1px solid ${theme.colors.neutral[200]}`,
        boxShadow: theme.shadows.sm,
      },
    }

    return {
      ...baseStyles,
      ...sizeStyles[size],
      ...variantStyles[variant],
    }
  }

  return (
    <button
      type={type}
      onClick={onClick}
      disabled={disabled}
      className={className}
      style={getStyles()}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      {icon}
      {children}
    </button>
  )
}












