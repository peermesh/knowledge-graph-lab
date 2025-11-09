import React, { createContext, useContext } from 'react'

export interface DesignTheme {
  colors: {
    primary: {
      50: string
      100: string
      500: string
      600: string
      700: string
    }
    accent: {
      100: string
      500: string
      700: string
    }
    secondary: {
      100: string
      500: string
      700: string
    }
    neutral: {
      50: string
      100: string
      200: string
      300: string
      400: string
      500: string
      600: string
      700: string
      800: string
      900: string
    }
    success: string
    warning: string
    error: string
    info: string
  }
  spacing: {
    xs: string
    sm: string
    md: string
    lg: string
    xl: string
    '2xl': string
  }
  borderRadius: {
    sm: string
    md: string
    lg: string
    xl: string
    full: string
  }
  shadows: {
    sm: string
    md: string
    lg: string
    xl: string
  }
  typography: {
    fontSize: {
      xs: string
      sm: string
      base: string
      lg: string
      xl: string
      '2xl': string
      '3xl': string
      '4xl': string
    }
    fontWeight: {
      normal: number
      medium: number
      semibold: number
      bold: number
      extrabold?: number
    }
  }
}

const ThemeContext = createContext<DesignTheme | null>(null)

export function ThemeProvider({ theme, children }: { theme: DesignTheme; children: React.ReactNode }) {
  return <ThemeContext.Provider value={theme}>{children}</ThemeContext.Provider>
}

export function useDesignTheme() {
  const theme = useContext(ThemeContext)
  if (!theme) {
    throw new Error('useDesignTheme must be used within a ThemeProvider')
  }
  return theme
}












