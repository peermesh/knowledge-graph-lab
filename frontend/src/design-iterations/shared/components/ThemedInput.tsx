import React from 'react'
import { useDesignTheme } from '../ThemeProvider'

interface ThemedInputProps {
  type?: 'text' | 'email' | 'password' | 'search' | 'number'
  placeholder?: string
  value: string
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void
  icon?: React.ReactNode
  className?: string
}

export function ThemedInput({
  type = 'text',
  placeholder,
  value,
  onChange,
  icon,
  className = '',
}: ThemedInputProps) {
  const theme = useDesignTheme()
  const [isFocused, setIsFocused] = React.useState(false)

  const containerStyles: React.CSSProperties = {
    position: 'relative',
    width: '100%',
  }

  const inputStyles: React.CSSProperties = {
    width: '100%',
    padding: icon ? '0.75rem 1rem 0.75rem 3rem' : '0.75rem 1rem',
    borderRadius: theme.borderRadius.md,
    fontSize: theme.typography.fontSize.sm,
    background: 'white',
    border: isFocused ? `2px solid ${theme.colors.primary[500]}` : `1px solid ${theme.colors.neutral[300]}`,
    color: theme.colors.neutral[900],
    outline: 'none',
    transition: 'all 200ms ease',
    boxShadow: isFocused ? `0 0 0 3px ${theme.colors.primary[500]}1A` : 'none',
  }

  const iconStyles: React.CSSProperties = {
    position: 'absolute',
    left: '1rem',
    top: '50%',
    transform: 'translateY(-50%)',
    color: theme.colors.neutral[400],
    pointerEvents: 'none',
  }

  return (
    <div style={containerStyles} className={className}>
      {icon && <div style={iconStyles}>{icon}</div>}
      <input
        type={type}
        placeholder={placeholder}
        value={value}
        onChange={onChange}
        style={inputStyles}
        onFocus={() => setIsFocused(true)}
        onBlur={() => setIsFocused(false)}
      />
    </div>
  )
}














