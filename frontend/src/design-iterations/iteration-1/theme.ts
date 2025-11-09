/**
 * Iteration 1: Modern Research Platform
 * 
 * Design Philosophy:
 * - Sophisticated and professional
 * - Deep indigo primary with vibrant teal accents
 * - Elevated cards with subtle shadows
 * - Modern typography with varied weights
 * - Refined spacing and visual rhythm
 */

export const theme = {
  colors: {
    // Primary Colors
    primary: {
      50: '#EEF2FF',
      100: '#E0E7FF',
      200: '#C7D2FE',
      300: '#A5B4FC',
      400: '#818CF8',
      500: '#4F46E5',  // Main primary
      600: '#4338CA',
      700: '#3730A3',
      800: '#312E81',
      900: '#1E1B4B',
    },
    
    // Accent - Teal
    accent: {
      50: '#F0FDFA',
      100: '#CCFBF1',
      200: '#99F6E4',
      300: '#5EEAD4',
      400: '#2DD4BF',
      500: '#14B8A6',  // Main accent
      600: '#0D9488',
      700: '#0F766E',
      800: '#115E59',
      900: '#134E4A',
    },
    
    // Secondary - Warm Amber
    secondary: {
      50: '#FFFBEB',
      100: '#FEF3C7',
      200: '#FDE68A',
      300: '#FCD34D',
      400: '#FBBF24',
      500: '#F59E0B',  // Main secondary
      600: '#D97706',
      700: '#B45309',
      800: '#92400E',
      900: '#78350F',
    },
    
    // Neutrals - Cool Gray
    neutral: {
      50: '#F8FAFC',
      100: '#F1F5F9',
      200: '#E2E8F0',
      300: '#CBD5E1',
      400: '#94A3B8',
      500: '#64748B',
      600: '#475569',
      700: '#334155',
      800: '#1E293B',
      900: '#0F172A',
    },
    
    // Semantic Colors
    success: '#10B981',
    warning: '#F59E0B',
    error: '#EF4444',
    info: '#3B82F6',
  },
  
  typography: {
    fontFamily: {
      sans: '"Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
      mono: '"JetBrains Mono", "Fira Code", Consolas, monospace',
    },
    
    fontSize: {
      xs: '0.75rem',      // 12px
      sm: '0.875rem',     // 14px
      base: '1rem',       // 16px
      lg: '1.125rem',     // 18px
      xl: '1.25rem',      // 20px
      '2xl': '1.5rem',    // 24px
      '3xl': '1.875rem',  // 30px
      '4xl': '2.25rem',   // 36px
    },
    
    fontWeight: {
      normal: 400,
      medium: 500,
      semibold: 600,
      bold: 700,
    },
    
    lineHeight: {
      tight: 1.25,
      normal: 1.5,
      relaxed: 1.75,
    },
  },
  
  spacing: {
    xs: '0.25rem',    // 4px
    sm: '0.5rem',     // 8px
    md: '1rem',       // 16px
    lg: '1.5rem',     // 24px
    xl: '2rem',       // 32px
    '2xl': '3rem',    // 48px
    '3xl': '4rem',    // 64px
  },
  
  borderRadius: {
    sm: '0.375rem',   // 6px
    md: '0.5rem',     // 8px
    lg: '0.75rem',    // 12px
    xl: '1rem',       // 16px
    full: '9999px',
  },
  
  shadows: {
    sm: '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
    md: '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
    lg: '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
    xl: '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)',
    inner: 'inset 0 2px 4px 0 rgba(0, 0, 0, 0.06)',
  },
  
  effects: {
    gradient: {
      primary: 'linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%)',
      accent: 'linear-gradient(135deg, #14B8A6 0%, #06B6D4 100%)',
      warm: 'linear-gradient(135deg, #F59E0B 0%, #EF4444 100%)',
    },
    blur: {
      sm: 'blur(4px)',
      md: 'blur(8px)',
      lg: 'blur(16px)',
    },
  },
}

// CSS Custom Properties for easy theming
export const cssVariables = `
  --v1-primary: ${theme.colors.primary[500]};
  --v1-primary-light: ${theme.colors.primary[100]};
  --v1-primary-dark: ${theme.colors.primary[700]};
  
  --v1-accent: ${theme.colors.accent[500]};
  --v1-accent-light: ${theme.colors.accent[100]};
  
  --v1-secondary: ${theme.colors.secondary[500]};
  
  --v1-neutral-50: ${theme.colors.neutral[50]};
  --v1-neutral-100: ${theme.colors.neutral[100]};
  --v1-neutral-200: ${theme.colors.neutral[200]};
  --v1-neutral-300: ${theme.colors.neutral[300]};
  --v1-neutral-400: ${theme.colors.neutral[400]};
  --v1-neutral-500: ${theme.colors.neutral[500]};
  --v1-neutral-600: ${theme.colors.neutral[600]};
  --v1-neutral-700: ${theme.colors.neutral[700]};
  --v1-neutral-800: ${theme.colors.neutral[800]};
  --v1-neutral-900: ${theme.colors.neutral[900]};
  
  --v1-success: ${theme.colors.success};
  --v1-warning: ${theme.colors.warning};
  --v1-error: ${theme.colors.error};
  --v1-info: ${theme.colors.info};
  
  --v1-radius-sm: ${theme.borderRadius.sm};
  --v1-radius-md: ${theme.borderRadius.md};
  --v1-radius-lg: ${theme.borderRadius.lg};
  --v1-radius-xl: ${theme.borderRadius.xl};
  
  --v1-shadow-sm: ${theme.shadows.sm};
  --v1-shadow-md: ${theme.shadows.md};
  --v1-shadow-lg: ${theme.shadows.lg};
  --v1-shadow-xl: ${theme.shadows.xl};
`












