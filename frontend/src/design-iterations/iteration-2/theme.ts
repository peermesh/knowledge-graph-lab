/**
 * Iteration 2: Bold Knowledge Hub
 * 
 * Design Philosophy:
 * - Confident and dynamic
 * - Navy blue primary with electric blue and coral accents
 * - Strong contrast and geometric precision
 * - Bold borders and high visual impact
 * - Action-oriented and data-driven
 */

export const theme = {
  colors: {
    // Primary Colors - Navy
    primary: {
      50: '#EFF6FF',
      100: '#DBEAFE',
      200: '#BFDBFE',
      300: '#93C5FD',
      400: '#60A5FA',
      500: '#1E3A8A',  // Main primary (Navy)
      600: '#1E40AF',
      700: '#1D4ED8',
      800: '#1E3A8A',
      900: '#172554',
    },
    
    // Accent - Electric Blue
    accent: {
      50: '#EFF6FF',
      100: '#DBEAFE',
      200: '#BFDBFE',
      300: '#93C5FD',
      400: '#60A5FA',
      500: '#3B82F6',  // Main accent (Electric Blue)
      600: '#2563EB',
      700: '#1D4ED8',
      800: '#1E40AF',
      900: '#1E3A8A',
    },
    
    // Secondary - Coral Pink
    secondary: {
      50: '#FFF1F2',
      100: '#FFE4E6',
      200: '#FECDD3',
      300: '#FDA4AF',
      400: '#FB7185',  
      500: '#FB7185',  // Main secondary (Coral)
      600: '#F43F5E',
      700: '#E11D48',
      800: '#BE123C',
      900: '#9F1239',
    },
    
    // Neutrals - True Gray
    neutral: {
      50: '#FAFAFA',
      100: '#F4F4F5',
      200: '#E4E4E7',
      300: '#D4D4D8',
      400: '#A1A1AA',
      500: '#71717A',
      600: '#52525B',
      700: '#3F3F46',
      800: '#27272A',
      900: '#18181B',
    },
    
    // Semantic Colors
    success: '#22C55E',
    warning: '#EAB308',
    error: '#DC2626',
    info: '#3B82F6',
  },
  
  typography: {
    fontFamily: {
      sans: '"Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
      display: '"Poppins", "Inter", sans-serif',
      mono: '"JetBrains Mono", monospace',
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
      extrabold: 800,
    },
    
    lineHeight: {
      tight: 1.2,
      normal: 1.5,
      relaxed: 1.75,
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
    sm: '0.25rem',    // More angular
    md: '0.375rem',
    lg: '0.5rem',
    xl: '0.75rem',
    full: '9999px',
  },
  
  shadows: {
    sm: '0 1px 3px 0 rgba(0, 0, 0, 0.1)',
    md: '0 4px 8px 0 rgba(0, 0, 0, 0.12)',
    lg: '0 8px 16px 0 rgba(0, 0, 0, 0.15)',
    xl: '0 16px 32px 0 rgba(0, 0, 0, 0.18)',
    inner: 'inset 0 2px 4px 0 rgba(0, 0, 0, 0.1)',
  },
  
  effects: {
    gradient: {
      primary: 'linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%)',
      accent: 'linear-gradient(135deg, #3B82F6 0%, #06B6D4 100%)',
      warm: 'linear-gradient(135deg, #FB7185 0%, #F43F5E 100%)',
    },
    blur: {
      sm: 'blur(4px)',
      md: 'blur(8px)',
      lg: 'blur(16px)',
    },
  },
}

export const cssVariables = `
  --v2-primary: ${theme.colors.primary[500]};
  --v2-primary-light: ${theme.colors.primary[100]};
  --v2-primary-dark: ${theme.colors.primary[800]};
  
  --v2-accent: ${theme.colors.accent[500]};
  --v2-accent-light: ${theme.colors.accent[100]};
  
  --v2-secondary: ${theme.colors.secondary[500]};
  
  --v2-neutral-50: ${theme.colors.neutral[50]};
  --v2-neutral-100: ${theme.colors.neutral[100]};
  --v2-neutral-200: ${theme.colors.neutral[200]};
  --v2-neutral-300: ${theme.colors.neutral[300]};
  --v2-neutral-400: ${theme.colors.neutral[400]};
  --v2-neutral-500: ${theme.colors.neutral[500]};
  --v2-neutral-600: ${theme.colors.neutral[600]};
  --v2-neutral-700: ${theme.colors.neutral[700]};
  --v2-neutral-800: ${theme.colors.neutral[800]};
  --v2-neutral-900: ${theme.colors.neutral[900]};
  
  --v2-success: ${theme.colors.success};
  --v2-warning: ${theme.colors.warning};
  --v2-error: ${theme.colors.error};
  --v2-info: ${theme.colors.info};
`














