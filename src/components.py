"""
SmartCoach Pro - Reusable UI Components
Standardized components for consistent layout and styling
"""

import streamlit as st
from typing import Optional, Callable, Dict, Any, List
from src.design_system import COLORS, SPACING, RADIUS, SHADOWS, GRADIENTS, TYPOGRAPHY


def render_page_header(title: str, subtitle: Optional[str] = None, icon: Optional[str] = None):
    """
    Render a consistent page header
    
    Args:
        title: Main heading text
        subtitle: Optional subtitle text
        icon: Optional icon (for special cases, not recommended for professional look)
    """
    icon_html = f"<span style='margin-right: 1rem;'>{icon}</span>" if icon else ""
    subtitle_html = f"<p style='font-size: 1.25rem; color: {COLORS['text_secondary']}; margin-top: 0.5rem;'>{subtitle}</p>" if subtitle else ""
    
    st.markdown(f"""
    <div class='glass-card' style='margin-bottom: {SPACING['xl']}'>
        <h1>{icon_html}{title}</h1>
        {subtitle_html}
    </div>
    """, unsafe_allow_html=True)


def render_metric_card(
    label: str, 
    value: str, 
    delta: Optional[str] = None,
    delta_positive: bool = True,
    color: Optional[str] = None
):
    """
    Render a professional metric card
    
    Args:
        label: Metric label
        value: Metric value
        delta: Optional change indicator
        delta_positive: Whether delta is positive (green) or negative (red)
        color: Optional custom border color
    """
    border_color = color or COLORS['primary']
    delta_color = COLORS['success'] if delta_positive else COLORS['danger']
    delta_html = f"<div style='color: {delta_color}; font-size: 0.9rem; margin-top: 0.25rem;'>{delta}</div>" if delta else ""
    
    st.markdown(f"""
    <div style='
        background: linear-gradient(135deg, rgba(99,102,241,0.08), rgba(139,92,246,0.08));
        backdrop-filter: blur(15px);
        border: 1.5px solid {border_color}40;
        border-radius: {RADIUS['xl']};
        padding: {SPACING['xl']};
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    '>
        <div style='
            color: {COLORS['text_tertiary']};
            font-weight: 700;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 0.5rem;
        '>{label}</div>
        <div style='
            font-size: 2.5rem;
            font-weight: 900;
            background: {GRADIENTS['text']};
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.25rem;
        '>{value}</div>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)


def render_glass_card(title: Optional[str] = None, start_open: bool = True):
    """
    Render a glass morphism card container
    Use with context manager for clean syntax
    
    Args:
        title: Optional card title
        start_open: If True, renders opening tag, if False renders closing tag
    """
    if start_open:
        title_html = f"<h3 style='margin-bottom: {SPACING['l']};'>{title}</h3>" if title else ""
        st.markdown(f"""
        <div class='glass-card'>
            {title_html}
        """, unsafe_allow_html=True)
    else:
        st.markdown("</div>", unsafe_allow_html=True)


def render_empty_state(
    message: str,
    icon: str = "📭",
    action_text: Optional[str] = None,
    action_key: Optional[str] = None
) -> bool:
    """
    Render an empty state with optional action button
    
    Args:
        message: Empty state message
        icon: Icon to display
        action_text: Optional call-to-action button text
        action_key: Unique key for the button
        
    Returns:
        True if action button was clicked, False otherwise
    """
    st.markdown(f"""
    <div style='
        text-align: center;
        padding: {SPACING['4xl']} {SPACING['xl']};
        background: {GRADIENTS['card']};
        border-radius: {RADIUS['2xl']};
        border: 1px solid {COLORS['border_subtle']};
    '>
        <div style='font-size: 4rem; margin-bottom: {SPACING['l']};'>{icon}</div>
        <h3 style='color: {COLORS['text_secondary']}; font-weight: 500;'>{message}</h3>
    </div>
    """, unsafe_allow_html=True)
    
    if action_text and action_key:
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            return st.button(action_text, key=action_key, use_container_width=True)
    return False


def render_loading_state(message: str = "Loading..."):
    """Render a loading state with spinner"""
    st.markdown(f"""
    <div style='
        text-align: center;
        padding: {SPACING['3xl']};
        color: {COLORS['text_secondary']};
    '>
        <div class='loading-spinner'></div>
        <p style='margin-top: {SPACING['l']};'>{message}</p>
    </div>
    """, unsafe_allow_html=True)


def render_stat_summary(stats: Dict[str, Any], columns: int = 4):
    """
    Render a row of statistics
    
    Args:
        stats: Dictionary with format {'label': 'value', ...}
        columns: Number of columns to use
    """
    cols = st.columns(columns)
    for i, (label, value) in enumerate(stats.items()):
        with cols[i % columns]:
            st.metric(label, value)


def render_success_message(message: str, icon: str = "✅"):
    """Render a success message"""
    st.markdown(f"""
    <div style='
        background: rgba(16, 185, 129, 0.1);
        border-left: 4px solid {COLORS['success']};
        padding: {SPACING['l']} {SPACING['xl']};
        border-radius: {RADIUS['m']};
        color: {COLORS['success']};
        margin: {SPACING['m']} 0;
    '>
        <strong>{icon} {message}</strong>
    </div>
    """, unsafe_allow_html=True)


def render_error_message(message: str, icon: str = "❌"):
    """Render an error message"""
    st.markdown(f"""
    <div style='
        background: rgba(239, 68, 68, 0.1);
        border-left: 4px solid {COLORS['danger']};
        padding: {SPACING['l']} {SPACING['xl']};
        border-radius: {RADIUS['m']};
        color: {COLORS['danger']};
        margin: {SPACING['m']} 0;
    '>
        <strong>{icon} {message}</strong>
    </div>
    """, unsafe_allow_html=True)


def render_info_message(message: str, icon: str = "ℹ️"):
    """Render an info message"""
    st.markdown(f"""
    <div style='
        background: rgba(59, 130, 246, 0.1);
        border-left: 4px solid {COLORS['info']};
        padding: {SPACING['l']} {SPACING['xl']};
        border-radius: {RADIUS['m']};
        color: {COLORS['info']};
        margin: {SPACING['m']} 0;
    '>
        <strong>{icon} {message}</strong>
    </div>
    """, unsafe_allow_html=True)


def render_warning_message(message: str, icon: str = "⚠️"):
    """Render a warning message"""
    st.markdown(f"""
    <div style='
        background: rgba(245, 158, 11, 0.1);
        border-left: 4px solid {COLORS['warning']};
        padding: {SPACING['l']} {SPACING['xl']};
        border-radius: {RADIUS['m']};
        color: {COLORS['warning']};
        margin: {SPACING['m']} 0;
    '>
        <strong>{icon} {message}</strong>
    </div>
    """, unsafe_allow_html=True)


def render_section_divider(text: Optional[str] = None):
    """Render a section divider with optional text"""
    if text:
        st.markdown(f"""
        <div style='
            display: flex;
            align-items: center;
            margin: {SPACING['2xl']} 0;
            color: {COLORS['text_tertiary']};
            font-size: 0.875rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
        '>
            <div style='flex: 1; height: 1px; background: {COLORS['border_subtle']};'></div>
            <div style='padding: 0 {SPACING['l']};'>{text}</div>
            <div style='flex: 1; height: 1px; background: {COLORS['border_subtle']};'></div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style='
            height: 1px;
            background: {COLORS['border_subtle']};
            margin: {SPACING['2xl']} 0;
        '></div>
        """, unsafe_allow_html=True)


def render_badge(text: str, color: str = None, variant: str = "primary"):
    """
    Render a small badge
    
    Args:
        text: Badge text
        color: Custom color (hex)
        variant: 'primary', 'success', 'warning', 'danger', 'info'
    """
    color_map = {
        'primary': COLORS['primary'],
        'success': COLORS['success'],
        'warning': COLORS['warning'],
        'danger': COLORS['danger'],
        'info': COLORS['info'],
    }
    badge_color = color or color_map.get(variant, COLORS['primary'])
    
    st.markdown(f"""
    <span style='
        display: inline-block;
        background: {badge_color}20;
        color: {badge_color};
        padding: 0.25rem 0.75rem;
        border-radius: {RADIUS['full']};
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    '>{text}</span>
    """, unsafe_allow_html=True)


def render_progress_bar(value: float, max_value: float = 100, label: Optional[str] = None, show_percentage: bool = True):
    """
    Render a progress bar using Streamlit's native component
    
    Args:
        value: Current value
        max_value: Maximum value
        label: Optional label above the progress bar
        show_percentage: Whether to show percentage text
    """
    percentage = min((value / max_value), 1.0)
    
    if label:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.caption(label)
        if show_percentage:
            with col2:
                st.caption(f"{percentage*100:.0f}%")
    elif show_percentage:
        st.caption(f"{percentage*100:.0f}%")
    
    st.progress(percentage)


def render_card_grid(items: List[Dict[str, Any]], columns: int = 3):
    """
    Render items in a grid of cards
    
    Args:
        items: List of dicts with 'title', 'content', 'footer' keys
        columns: Number of columns
    """
    cols = st.columns(columns)
    for i, item in enumerate(items):
        with cols[i % columns]:
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            if 'title' in item:
                st.markdown(f"### {item['title']}")
            if 'content' in item:
                st.write(item['content'])
            if 'footer' in item:
                st.caption(item['footer'])
            st.markdown("</div>", unsafe_allow_html=True)
