# SmartCoach Pro - Professional Fitness Application
# Refactored with modular architecture and external CSS
# Updated: 2026-01-04 - Login Page Redesign

import streamlit as st
import base64
from pathlib import Path
import logging

# Import pages
from pages import dashboard_page, workout_page, programs_page, achievements_page, history_page

# Import authentication
from backend.auth import login_user, register_user
from backend.session_manager import get_session_manager

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="SmartCoach Pro",
    layout="wide",
    initial_sidebar_state="expanded"
)


@st.cache_data
def get_img_b64(path: str) -> str:
    """Load and encode image as base64 - Cached for performance"""
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except FileNotFoundError:
        logger.warning(f"Image file not found: {path}")
        return ""
    except Exception as e:
        logger.error(f"Error loading image {path}: {str(e)}")
        return ""


# Load background images
LOGIN_BG = get_img_b64('assets/login_bg_premium.png')
DASH_BG = get_img_b64('assets/dashboard_background_pro_1767472546043.png')
WORKOUT_BG = get_img_b64('assets/workout_background_pro_1767472562531.png')
ACH_BG = get_img_b64('assets/achievements_background_pro_1767472580234.png')


def load_css_content():
    """Load external CSS file content - Fresh load every time for now"""
    css_file = Path("styles.css")
    if css_file.exists():
        try:
            with open(css_file, 'r', encoding='utf-8') as f:
                css = f.read()
            # CSS now has !important declarations to override Streamlit
            return css
        except Exception as e:
            logger.error(f"Error loading CSS file: {str(e)}")
            return get_fallback_css()
    else:
        logger.warning("CSS file not found, using fallback")
        return get_fallback_css()


def get_fallback_css():
    """Return fallback CSS if main file is not available"""
    return """
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
        * {font-family: 'Inter', sans-serif;}
        #MainMenu, footer, header, .stDeployButton {display: none !important;}
        .main {background: #0a0e1a !important;}
    """


def load_css():
    """Inject CSS into page - called on every page load"""
    css_content = load_css_content()
    # Use a style tag with higher specificity
    st.markdown(f"""
    <style>
    {css_content}
    </style>
    """, unsafe_allow_html=True)


def init_session_state():
    """Initialize session state variables with persistence check"""
    # Try to restore session from query params (simulating cookie)
    session_mgr = get_session_manager()
    
    # Check if we have a session token in query params
    query_params = st.query_params
    session_token = query_params.get('session', None)
    
    if session_token and 'user_id' not in st.session_state:
        # Try to restore session
        user = session_mgr.get_user_by_token(session_token)
        if user:
            st.session_state.user_id = user.id
            st.session_state.user = user
            logger.info(f"Session restored for user: {user.username}")
    
    # Initialize defaults for missing keys
    defaults = {
        'user_id': None,
        'user': None,
        'page': 'dashboard',
        'classifier': None,
        'workout_started': False,
        'session_token': session_token
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def set_background(img_b64: str):
    """Set page background image"""
    if img_b64:
        st.markdown(
            f"""<div class='bg-overlay' style='background-image: url(data:image/png;base64,{img_b64})'></div>""",
            unsafe_allow_html=True
        )


def login_page():
    """Render ultra-modern professional login page"""
    set_background(LOGIN_BG)
    
    # Create centered layout with professional card
    col1, col2, col3 = st.columns([1.2, 2, 1.2])
    
    with col2:
        # Premium Brand Header
        st.markdown("""
        <div class='login-container'>
            <div class='brand-header'>
                <h1 class='brand-title'>SmartCoach Pro</h1>
                <p class='brand-subtitle'>AI-Powered Athletic Training</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Modern Tabs with enhanced styling
        tab1, tab2 = st.tabs(["Sign In", "Create Account"])
        
        with tab1:
            st.markdown("""
            <div class='form-section'>
                <h2 class='form-title'>Welcome Back</h2>
                <p class='form-description'>Sign in to continue your fitness journey</p>
            </div>
            """, unsafe_allow_html=True)
            
            with st.form("login_form", clear_on_submit=False):
                st.markdown("<div class='input-group'>", unsafe_allow_html=True)
                username = st.text_input(
                    "Username or Email",
                    placeholder="Enter your username or email",
                    key="login_username"
                )
                st.markdown("</div>", unsafe_allow_html=True)
                
                st.markdown("<div class='input-group'>", unsafe_allow_html=True)
                password = st.text_input(
                    "Password",
                    type="password",
                    placeholder="Enter your password",
                    key="login_password"
                )
                st.markdown("</div>", unsafe_allow_html=True)
                
                st.markdown("<div style='height: 2rem'></div>", unsafe_allow_html=True)
                
                submitted = st.form_submit_button(
                    "Sign In",
                    use_container_width=True,
                    type="primary"
                )
                
                if submitted:
                    if username and password:
                        success, message, user = login_user(username, password)
                        if success:
                            # Create session token
                            session_mgr = get_session_manager()
                            token = session_mgr.create_session(user.id)
                            
                            st.session_state.update({
                                'user_id': user.id,
                                'user': user,
                                'page': 'dashboard',
                                'session_token': token
                            })
                            
                            # Add token to URL for persistence
                            st.query_params['session'] = token
                            
                            st.success("Login successful! Welcome back!")
                            st.rerun()
                        else:
                            st.error(message)
                    else:
                        st.warning("Please enter both username and password")
        
        with tab2:
            st.markdown("""
            <div class='form-section'>
                <h2 class='form-title'>Create Your Account</h2>
                <p class='form-description'>Join SmartCoach Pro and start training smarter</p>
            </div>
            """, unsafe_allow_html=True)
            
            with st.form("register_form", clear_on_submit=False):
                st.markdown("<div class='input-group'>", unsafe_allow_html=True)
                new_username = st.text_input(
                    "Username",
                    placeholder="Choose a unique username",
                    key="register_username"
                )
                st.markdown("</div>", unsafe_allow_html=True)
                
                st.markdown("<div class='input-group'>", unsafe_allow_html=True)
                new_email = st.text_input(
                    "Email",
                    placeholder="your.email@example.com",
                    key="register_email"
                )
                st.markdown("</div>", unsafe_allow_html=True)
                
                st.markdown("<div class='input-group'>", unsafe_allow_html=True)
                new_password = st.text_input(
                    "Password",
                    type="password",
                    placeholder="Create a strong password (min. 8 characters)",
                    key="register_password"
                )
                st.markdown("</div>", unsafe_allow_html=True)
                
                # Password strength indicator
                if new_password:
                    from backend.security import check_password_strength
                    strength_score, description = check_password_strength(new_password)
                    colors = {
                        0: "#ef4444", 1: "#f59e0b", 2: "#eab308", 
                        3: "#22c55e", 4: "#10b981"
                    }
                    color = colors.get(strength_score, "#ef4444")
                    width = (strength_score + 1) * 20
                    
                    st.markdown(f"""
                    <div style="margin-bottom: 1.5rem;">
                        <div style="width: 100%; height: 6px; background: rgba(255,255,255,0.1); border-radius: 999px; overflow: hidden; margin-bottom: 0.5rem;">
                            <div style="width: {width}%; height: 100%; background: {color}; transition: all 0.3s ease; border-radius: 999px;"></div>
                        </div>
                        <div style="font-size: 0.75rem; color: {color}; font-weight: 600;">
                            {description}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("<div class='input-group'>", unsafe_allow_html=True)
                confirm_password = st.text_input(
                    "Confirm Password",
                    type="password",
                    placeholder="Re-enter your password",
                    key="register_confirm"
                )
                st.markdown("</div>", unsafe_allow_html=True)
                
                st.markdown("<div style='height: 2rem'></div>", unsafe_allow_html=True)
                
                submitted = st.form_submit_button(
                    "Create Account",
                    use_container_width=True,
                    type="primary"
                )
                
                if submitted:
                    if new_username and new_email and new_password and confirm_password:
                        if new_password != confirm_password:
                            st.error("Passwords do not match!")
                        else:
                            success, message, _ = register_user(new_username, new_email, new_password)
                            if success:
                                st.success(f"{message}")
                                st.info("Please go to the 'Sign In' tab to login with your credentials")
                            else:
                                st.error(message)
                    else:
                        st.warning("Please fill in all fields")
        
        # Professional Footer
        st.markdown("""
            <div class='login-footer'>
                <p>Powered by Advanced AI Technology</p>
            </div>
        </div>
        """, unsafe_allow_html=True)



def render_sidebar():
    """Render modern navigation sidebar"""
    with st.sidebar:
        # Modern App Header
        st.markdown("""
        <div style='
            text-align: center;
            padding: 2rem 1rem;
            margin-bottom: 1rem;
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.15), rgba(139, 92, 246, 0.1));
            border-radius: 1rem;
            border: 1px solid rgba(99, 102, 241, 0.2);
        '>
            <h1 style='
                font-size: 1.8rem;
                font-weight: 900;
                margin: 0;
                background: linear-gradient(135deg, #ffffff, #6366f1);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            '>SmartCoach Pro</h1>
            <p style='color: rgba(255,255,255,0.6); font-size: 0.8rem; margin-top: 0.5rem'>
                AI-Powered Fitness
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<div style='height: 1rem'></div>", unsafe_allow_html=True)
        
        # Navigation items - clean text only
        pages = [
            ('dashboard', 'Dashboard'),
            ('workout', 'Workout'),
            ('programs', 'Programs'),
            ('achievements', 'Achievements'),
            ('history', 'History')
        ]
        
        current_page = st.session_state.get('page', 'dashboard')
        
        for page_key, page_label in pages:
            # Highlight current page
            is_active = current_page == page_key
            if is_active:
                st.markdown(f"""
                <div style='
                    background: linear-gradient(90deg, rgba(99, 102, 241, 0.3), transparent);
                    border-left: 3px solid #6366f1;
                    padding: 0.75rem 1rem;
                    margin-bottom: 0.5rem;
                    border-radius: 0 0.5rem 0.5rem 0;
                '>
                    <span style='color: #ffffff; font-weight: 600'>{page_label}</span>
                </div>
                """, unsafe_allow_html=True)
            else:
                if st.button(page_label, key=f"nav_{page_key}", use_container_width=True):
                    st.session_state.page = page_key
                    st.rerun()
        
        st.markdown("<div style='height: 2rem'></div>", unsafe_allow_html=True)
        st.markdown("---")
        
        # User section
        st.markdown(f"""
        <div style='
            text-align: center;
            padding: 1.5rem 1rem;
            background: rgba(255,255,255,0.05);
            border-radius: 1rem;
            margin-top: 1rem;
        '>
            <div style='
                width: 50px;
                height: 50px;
                background: linear-gradient(135deg, #6366f1, #8b5cf6);
                border-radius: 50%;
                margin: 0 auto 0.75rem;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 1.5rem;
            '>U</div>
            <p style='color: #f1f5f9; font-weight: 600; margin: 0'>{st.session_state.user.username}</p>
            <p style='color: rgba(255,255,255,0.5); font-size: 0.75rem; margin-top: 0.25rem'>Member</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<div style='height: 1rem'></div>", unsafe_allow_html=True)
        
        
        if st.button("Logout", key="logout_btn", use_container_width=True):
            # Revoke session token if exists
            if 'session_token' in st.session_state and st.session_state.session_token:
                session_mgr = get_session_manager()
                session_mgr.revoke_session(st.session_state.session_token)
            
            # Clear ALL session state
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            
            # Clear query params (removes session token from URL)
            st.query_params.clear()
            
            # Rerun will now show login page because user_id is None
            st.rerun()


def main_app():
    """Main application with navigation"""
    render_sidebar()
    
    # Route to appropriate page
    page = st.session_state.get('page', 'dashboard')
    
    if page == 'dashboard':
        dashboard_page(DASH_BG)
    elif page == 'workout':
        workout_page(WORKOUT_BG)
    elif page == 'programs':
        programs_page(DASH_BG)
    elif page == 'achievements':
        achievements_page(ACH_BG)
    elif page == 'history':
        history_page(DASH_BG)
    else:
        # Default to dashboard
        dashboard_page(DASH_BG)


def main():
    """Application entry point"""
    # Load external CSS
    load_css()
    
    # Initialize session state
    init_session_state()
    
    # Route based on authentication status
    if st.session_state.user_id is None:
        login_page()
    else:
        main_app()


if __name__ == "__main__":
    main()
