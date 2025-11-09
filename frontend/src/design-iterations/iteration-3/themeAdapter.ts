import { theme as rawTheme } from './theme'
import type { DesignTheme } from '../shared/ThemeProvider'

export const iteration3Theme: DesignTheme = {
  colors: {
    primary: {
      50: rawTheme.colors.primary[50],
      100: rawTheme.colors.primary[100],
      500: rawTheme.colors.primary[500],
      600: rawTheme.colors.primary[600],
      700: rawTheme.colors.primary[700],
    },
    accent: {
      100: rawTheme.colors.accent[100],
      500: rawTheme.colors.accent[500],
      700: rawTheme.colors.accent[700],
    },
    secondary: {
      100: rawTheme.colors.secondary[100],
      500: rawTheme.colors.secondary[500],
      700: rawTheme.colors.secondary[700],
    },
    neutral: {
      50: rawTheme.colors.neutral[50],
      100: rawTheme.colors.neutral[100],
      200: rawTheme.colors.neutral[200],
      300: rawTheme.colors.neutral[300],
      400: rawTheme.colors.neutral[400],
      500: rawTheme.colors.neutral[500],
      600: rawTheme.colors.neutral[600],
      700: rawTheme.colors.neutral[700],
      800: rawTheme.colors.neutral[800],
      900: rawTheme.colors.neutral[900],
    },
    success: rawTheme.colors.success,
    warning: rawTheme.colors.warning,
    error: rawTheme.colors.error,
    info: rawTheme.colors.info,
  },
  spacing: {
    xs: rawTheme.spacing.xs,
    sm: rawTheme.spacing.sm,
    md: rawTheme.spacing.md,
    lg: rawTheme.spacing.lg,
    xl: rawTheme.spacing.xl,
    '2xl': rawTheme.spacing['2xl'],
  },
  borderRadius: {
    sm: rawTheme.borderRadius.sm,
    md: rawTheme.borderRadius.md,
    lg: rawTheme.borderRadius.lg,
    xl: rawTheme.borderRadius.xl,
    full: rawTheme.borderRadius.full,
  },
  shadows: {
    sm: rawTheme.shadows.sm,
    md: rawTheme.shadows.md,
    lg: rawTheme.shadows.lg,
    xl: rawTheme.shadows.xl,
  },
  typography: {
    fontSize: {
      xs: rawTheme.typography.fontSize.xs,
      sm: rawTheme.typography.fontSize.sm,
      base: rawTheme.typography.fontSize.base,
      lg: rawTheme.typography.fontSize.lg,
      xl: rawTheme.typography.fontSize.xl,
      '2xl': rawTheme.typography.fontSize['2xl'],
      '3xl': rawTheme.typography.fontSize['3xl'],
      '4xl': rawTheme.typography.fontSize['4xl'],
    },
    fontWeight: {
      normal: rawTheme.typography.fontWeight.normal,
      medium: rawTheme.typography.fontWeight.medium,
      semibold: rawTheme.typography.fontWeight.semibold,
      bold: rawTheme.typography.fontWeight.bold,
    },
  },
}














