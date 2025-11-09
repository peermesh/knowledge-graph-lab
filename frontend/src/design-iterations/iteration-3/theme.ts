/**
 * Iteration 3: Warm Discovery Space
 * 
 * Design Philosophy:
 * - Inviting and approachable
 * - Sage green primary with warm amber and soft purple accents
 * - Organic shapes and friendly rounded corners
 * - Playful yet professional
 * - Focus on content discovery and exploration
 */

export const theme = {
  colors: {
    // Primary Colors - Sage Green
    primary: {
      50: '#F0FDF4',
      100: '#DCFCE7',
      200: '#BBF7D0',
      300: '#86EFAC',
      400: '#4ADE80',
      500: '#10B981',  // Main primary (Sage Green)
      600: '#059669',
      700: '#047857',
      800: '#065F46',
      900: '#064E3B',
    },
    
    // Accent - Warm Amber
    accent: {
      50: '#FFFBEB',
      100: '#FEF3C7',
      200: '#FDE68A',
      300: '#FCD34D',
      400: '#FBBF24',
      500: '#F59E0B',  // Main accent (Amber)
      600: '#D97706',
      700: '#B45309',
      800: '#92400E',
      900: '#78350F',
    },
    
    // Secondary - Soft Purple
    secondary: {
      50: '#FAF5FF',
      100: '#F3E8FF',
      200: '#E9D5FF',
      300: '#D8B4FE',
      400: '#C084FC',
      500: '#8B5CF6',  // Main secondary (Purple)
      600: '#7C3AED',
      700: '#6D28D9',
      800: '#5B21B6',
      900: '#4C1D95',
    },
    
    // Neutrals - Warm Gray
    neutral: {
      50: '#FAFAF9',
      100: '#F5F5F4',
      200: '#E7E5E4',
      300: '#D6D3D1',
      400: '#A8A29E',
      500: '#78716C',
      600: '#57534E',
      700: '#44403C',
      800: '#292524',
      900: '#1C1917',
    },
    
    // Semantic Colors
    success: '#10B981',
    warning: '#F59E0B',
    error: '#F87171',
    info: '#60A5FA',
  },
  
  typography: {
    fontFamily: {
      sans: '"Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
      display: '"Plus Jakarta Sans", "Inter", sans-serif',
      mono: '"Fira Code", monospace',
    },
    
    fontSize: {
      xs: '0.75rem',
      sm: '0.875rem',
      base: '1rem',
      lg: '1.125rem',
      xl: '1.25rem',
      '2xl': '1.5rem',
      '3xl': '1.875rem',
      '4xl': '2.25rem',
    },
    
    fontWeight: {
      normal: 400,
      medium: 500,
      semibold: 600,
      bold: 700,
    },
    
    lineHeight: {
      tight: 1.25,
      normal: 1.6,
      relaxed: 1.8,
    },
  },
  
  spacing: {
    xs: '0.25rem',
    sm: '0.5rem',
    md: '1rem',
    lg: '1.5rem',
    xl: '2rem',
    '2xl': '3rem',
    '3xl': '4rem',
  },
  
  borderRadius: {
    sm: '0.5rem',     // More rounded
    md: '0.75rem',
    lg: '1rem',
    xl: '1.5rem',
    full: '9999px',
  },
  
  shadows: {
    sm: '0 2px 4px 0 rgba(0, 0, 0, 0.06)',
    md: '0 4px 12px 0 rgba(0, 0, 0, 0.08)',
    lg: '0 8px 24px 0 rgba(0, 0, 0, 0.10)',
    xl: '0 16px 48px 0 rgba(0, 0, 0, 0.12)',
    inner: 'inset 0 2px 4px 0 rgba(0, 0, 0, 0.06)',
    colored: '0 8px 24px 0 rgba(16, 185, 129, 0.20)',  // Green shadow
  },
  
  effects: {
    gradient: {
      primary: 'linear-gradient(135deg, #10B981 0%, #34D399 100%)',
      accent: 'linear-gradient(135deg, #F59E0B 0%, #FBBF24 100%)',
      warm: 'linear-gradient(135deg, #8B5CF6 0%, #A78BFA 100%)',
    },
    blur: {
      sm: 'blur(8px)',
      md: 'blur(12px)',
      lg: 'blur(20px)',
    },
  },
}

export const cssVariables = `
  --v3-primary: ${theme.colors.primary[500]};
  --v3-primary-light: ${theme.colors.primary[100]};
  --v3-primary-dark: ${theme.colors.primary[700]};
  
  --v3-accent: ${theme.colors.accent[500]};
  --v3-accent-light: ${theme.colors.accent[100]};
  
  --v3-secondary: ${theme.colors.secondary[500]};
  
  --v3-neutral-50: ${theme.colors.neutral[50]};
  --v3-neutral-100: ${theme.colors.neutral[100]};
  --v3-neutral-200: ${theme.colors.neutral[200]};
  --v3-neutral-300: ${theme.colors.neutral[300]};
  --v3-neutral-400: ${theme.colors.neutral[400]};
  --v3-neutral-500: ${theme.colors.neutral[500]};
  --v3-neutral-600: ${theme.colors.neutral[600]};
  --v3-neutral-700: ${theme.colors.neutral[700]};
  --v3-neutral-800: ${theme.colors.neutral[800]};
  --v3-neutral-900: ${theme.colors.neutral[900]};
  
  --v3-success: ${theme.colors.success};
  --v3-warning: ${theme.colors.warning};
  --v3-error: ${theme.colors.error};
  --v3-info: ${theme.colors.info};
`














