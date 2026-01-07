"""
SmartCoach Pro - Design System
Centralized design tokens for consistent styling across the application
"""

# Color Palette
COLORS = {
    # Primary & Secondary
    'primary': '#6366f1',
    'primary_dark': '#4f46e5',
    'primary_darker': '#4338ca',
    'secondary': '#8b5cf6',
    'secondary_dark': '#7c3aed',
    'accent': '#ec4899',
    
    # Semantic Colors
    'success': '#10b981',
    'success_dark': '#059669',
    'warning': '#f59e0b',
    'warning_dark': '#d97706',
    'danger': '#ef4444',
    'danger_dark': '#dc2626',
    'info': '#3b82f6',
    'info_dark': '#2563eb',
    
    # Neutrals (Dark Theme)
    'neutral': {
        950: '#0a0e1a',
        900: '#0f1419',
        800: '#1a1f35',
        700: '#1e293b',
        600: '#334155',
        500: '#64748b',
        400: '#94a3b8',
        300: '#cbd5e1',
        200: '#e2e8f0',
        100: '#f1f5f9',
        50: '#f8fafc',
    },
    
    # Backgrounds
    'bg_dark': '#0a0e1a',
    'bg_surface': '#0f1419',
    'bg_surface_elevated': '#1a1f35',
    
    # Text
    'text_primary': 'rgba(255, 255, 255, 0.95)',
    'text_secondary': 'rgba(255, 255, 255, 0.85)',
    'text_tertiary': 'rgba(255, 255, 255, 0.7)',
    'text_disabled': 'rgba(255, 255, 255, 0.5)',
    
    # Borders & Dividers
    'border_subtle': 'rgba(255, 255, 255, 0.1)',
    'border_medium': 'rgba(255, 255, 255, 0.15)',
    'border_strong': 'rgba(255, 255, 255, 0.25)',
}

# Typography Scale
TYPOGRAPHY = {
    'font_family': "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
    'font_family_mono': "'Fira Code', 'Courier New', monospace",
    
    # Headings
    'heading1': {
        'size': '3rem',
        'weight': 900,
        'line_height': 1.1,
        'letter_spacing': '-1.5px',
    },
    'heading2': {
        'size': '2rem',
        'weight': 700,
        'line_height': 1.2,
        'letter_spacing': '-0.5px',
    },
    'heading3': {
        'size': '1.5rem',
        'weight': 600,
        'line_height': 1.3,
    },
    'heading4': {
        'size': '1.25rem',
        'weight': 600,
        'line_height': 1.4,
    },
    
    # Body Text
    'body_large': {
        'size': '1.125rem',
        'weight': 400,
        'line_height': 1.7,
    },
    'body': {
        'size': '1rem',
        'weight': 400,
        'line_height': 1.6,
    },
    'body_small': {
        'size': '0.875rem',
        'weight': 400,
        'line_height': 1.5,
    },
    
    # Special
    'caption': {
        'size': '0.75rem',
        'weight': 500,
        'line_height': 1.4,
        'letter_spacing': '0.5px',
    },
    'button': {
        'size': '1rem',
        'weight': 700,
        'letter_spacing': '0.5px',
    },
    'label': {
        'size': '0.875rem',
        'weight': 600,
        'letter_spacing': '0.5px',
    },
}

# Spacing Scale (rem-based)
SPACING = {
    'xs': '0.25rem',    # 4px
    's': '0.5rem',      # 8px
    'm': '1rem',        # 16px
    'l': '1.5rem',      # 24px
    'xl': '2rem',       # 32px
    '2xl': '2.5rem',    # 40px
    '3xl': '3rem',      # 48px
    '4xl': '4rem',      # 64px
    '5xl': '6rem',      # 96px
}

# Border Radius
RADIUS = {
    'xs': '0.25rem',    # 4px
    's': '0.5rem',      # 8px
    'm': '0.75rem',     # 12px
    'l': '1rem',        # 16px
    'xl': '1.25rem',    # 20px
    '2xl': '1.5rem',    # 24px
    'full': '9999px',
}

# Shadows
SHADOWS = {
    'xs': '0 1px 2px rgba(0, 0, 0, 0.05)',
    's': '0 2px 4px rgba(0, 0, 0, 0.1)',
    'm': '0 4px 8px rgba(0, 0, 0, 0.15)',
    'l': '0 8px 16px rgba(0, 0, 0, 0.2)',
    'xl': '0 12px 24px rgba(0, 0, 0, 0.25)',
    '2xl': '0 16px 32px rgba(0, 0, 0, 0.3)',
    
    # Colored shadows
    'primary': '0 6px 20px rgba(99, 102, 241, 0.5)',
    'primary_hover': '0 10px 30px rgba(99, 102, 241, 0.6)',
    'success': '0 4px 15px rgba(16, 185, 129, 0.4)',
    'glass': '0 8px 32px rgba(0, 0, 0, 0.4)',
    'glass_hover': '0 16px 48px rgba(99, 102, 241, 0.3)',
}

# Transitions
TRANSITIONS = {
    'fast': '0.15s cubic-bezier(0.4, 0, 0.2, 1)',
    'base': '0.3s cubic-bezier(0.4, 0, 0.2, 1)',
    'slow': '0.5s cubic-bezier(0.4, 0, 0.2, 1)',
    'bounce': '0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55)',
}

# Z-Index Scale
Z_INDEX = {
    'dropdown': 1000,
    'sticky': 1020,
    'fixed': 1030,
    'modal_backdrop': 1040,
    'modal': 1050,
    'popover': 1060,
    'tooltip': 1070,
}

# Breakpoints for Responsive Design
BREAKPOINTS = {
    'mobile': '480px',
    'tablet': '768px',
    'desktop': '1024px',
    'wide': '1280px',
    'ultra_wide': '1536px',
}

# Component Specific Tokens
COMPONENTS = {
    'button': {
        'padding': f"{SPACING['m']} {SPACING['xl']}",
        'border_radius': RADIUS['l'],
        'transition': TRANSITIONS['base'],
    },
    'card': {
        'padding': SPACING['2xl'],
        'border_radius': RADIUS['2xl'],
        'transition': TRANSITIONS['base'],
    },
    'input': {
        'padding': f"{SPACING['m']} {SPACING['l']}",
        'border_radius': RADIUS['l'],
        'border_width': '1.5px',
    },
    'metric_card': {
        'padding': SPACING['xl'],
        'border_radius': RADIUS['xl'],
        'border_width': '1.5px',
    },
}

# Glass Morphism Effects
GLASS = {
    'background': 'linear-gradient(135deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05))',
    'backdrop_filter': 'blur(20px) saturate(180%)',
    'border': f"1px solid {COLORS['border_medium']}",
}

# Gradients
GRADIENTS = {
    'primary': f"linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['primary_dark']} 100%)",
    'primary_hover': f"linear-gradient(135deg, {COLORS['primary_dark']} 0%, {COLORS['primary_darker']} 100%)",
    'secondary': f"linear-gradient(135deg, {COLORS['secondary']} 0%, {COLORS['secondary_dark']} 100%)",
    'success': f"linear-gradient(135deg, {COLORS['success']} 0%, {COLORS['success_dark']} 100%)",
    'text': f"linear-gradient(135deg, {COLORS['neutral'][50]} 0%, {COLORS['neutral'][300]} 100%)",
    'card': 'linear-gradient(180deg, #0f1419 0%, #1a1f35 100%)',
    'overlay': 'linear-gradient(135deg, rgba(10, 14, 26, 0.92) 0%, rgba(26, 31, 53, 0.88) 100%)',
    'progress': f"linear-gradient(90deg, {COLORS['primary']} 0%, {COLORS['secondary']} 50%, {COLORS['accent']} 100%)",
}

# Performance Levels Configuration
PERFORMANCE_LEVELS = {
    'excellent': {
        'threshold': 90,
        'label': 'EXCELLENT',
        'color': COLORS['success'],
        'icon': '🏆',
    },
    'very_good': {
        'threshold': 75,
        'label': 'VERY GOOD',
        'color': COLORS['secondary'],
        'icon': '💪',
    },
    'good': {
        'threshold': 60,
        'label': 'GOOD',
        'color': COLORS['info'],
        'icon': '👍',
    },
    'needs_improvement': {
        'threshold': 0,
        'label': 'NEEDS IMPROVEMENT',
        'color': COLORS['warning'],
        'icon': '⚡',
    },
}

def get_performance_level(score: float) -> dict:
    """Get performance level configuration based on score"""
    for level_key in ['excellent', 'very_good', 'good', 'needs_improvement']:
        level = PERFORMANCE_LEVELS[level_key]
        if score >= level['threshold']:
            return level
    return PERFORMANCE_LEVELS['needs_improvement']

def get_color_with_opacity(color: str, opacity: float) -> str:
    """Convert hex color to rgba with opacity"""
    # Simple helper - in production, use a proper color library
    return f"{color}{int(opacity * 255):02x}"
