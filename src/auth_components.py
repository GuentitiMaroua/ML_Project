"""
Modern authentication UI components for SmartCoach Pro
Includes password strength indicator, validation feedback, and loading states
"""
import streamlit as st
from backend.security import check_password_strength


def render_password_strength_indicator(password: str):
    """Render a visual password strength indicator"""
    if not password:
        return
    
    strength_score, description = check_password_strength(password)
    
    # Color mapping
    colors = {
        0: "#ef4444",  # red
        1: "#f59e0b",  # orange
        2: "#eab308",  # yellow
        3: "#22c55e",  # green
        4: "#10b981",  # strong green
    }
    
    color = colors.get(strength_score, "#ef4444")
    width_percent = (strength_score + 1) * 20  # 20, 40, 60, 80, 100%
    
    # Render strength bar
    st.markdown(f"""
    <div style="margin-top: 0.5rem; margin-bottom: 1rem;">
        <div style="
            width: 100%;
            height: 6px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 999px;
            overflow: hidden;
        ">
            <div style="
                width: {width_percent}%;
                height: 100%;
                background: {color};
                transition: all 0.3s ease;
                border-radius: 999px;
            "></div>
        </div>
        <div style="
            margin-top: 0.25rem;
            font-size: 0.75rem;
            color: {color};
            font-weight: 600;
        ">
            {description}
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_input_with_icon(label: str, input_type: str ="text", placeholder: str = "", key: str = "", icon: str = ""):
    """Render a modern input field with icon"""
    icon_html = f"<span style='margin-right: 0.75rem; font-size: 1.2rem;'>{icon}</span>" if icon else ""
    
    st.markdown(f"""
    <div style="margin-bottom: 1.5rem;">
        <label style="
            display: block;
            font-weight: 600;
            margin-bottom: 0.5rem;
            color: rgba(255, 255, 255, 0.9);
            font-size: 0.875rem;
        ">
            {icon_html}{label}
        </label>
    </div>
    """, unsafe_allow_html=True)
    
    if input_type == "password":
        # Password with show/hide toggle
        col1, col2 = st.columns([10, 1])
        with col1:
            value = st.text_input(
                label,
                type="password",
                placeholder=placeholder,
                key=key,
                label_visibility="collapsed"
            )
        return value
    else:
        return st.text_input(
            label,
            placeholder=placeholder,
            key=key,
            label_visibility="collapsed"
        )


def render_loading_button(text: str, is_loading: bool = False, key: str = ""):
    """Render a button with loading state"""
    if is_loading:
        st.markdown(f"""
        <button style="
            width: 100%;
            padding: 1rem;
            background: linear-gradient(135deg, #6366f1, #8b5cf6);
            color: white;
            border: none;
            border-radius: 0.75rem;
            font-weight: 700;
            font-size: 1rem;
            cursor: not-allowed;
            opacity: 0.7;
            display: flex;
            align-items: center;
            justify-content: center;
        ">
            <div class="spinner" style="
                width: 16px;
                height: 16px;
                border: 2px solid rgba(255,255,255,0.3);
                border-top-color: white;
                border-radius: 50%;
                animation: spin 0.6s linear infinite;
                margin-right: 0.5rem;
            "></div>
            Loading...
        </button>
        <style>
        @keyframes spin {{
            to {{ transform: rotate(360deg); }}
        }}
        </style>
        """, unsafe_allow_html=True)
        return False
    else:
        return st.button(text, use_container_width=True, type="primary", key=key)
