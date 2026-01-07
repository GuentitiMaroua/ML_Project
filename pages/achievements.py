"""
Achievements Page - Professional & Clean
Modern design with clear organization
"""

import streamlit as st
from src.gamification import get_user_achievements
from src.design_system import COLORS


def set_background(img_b64):
    """Set page background image"""
    if img_b64:
        st.markdown(
            f"""<div class='bg-overlay' style='background-image: url(data:image/png;base64,{img_b64})'></div>""",
            unsafe_allow_html=True
        )


def achievements_page(background_b64=None):
    """Render the professional achievements page"""
    set_background(background_b64)
    
    # ==========================================
    # HERO SECTION
    # ==========================================
    st.markdown("""
    <div style='text-align: center; padding: 2rem 0 1rem 0; margin-bottom: 2rem; border-bottom: 1px solid rgba(255,255,255,0.1);'>
        <h1 style='font-size: 2.5rem; font-weight: 800; margin-bottom: 0.5rem; 
                   background: linear-gradient(135deg, #ffffff 0%, #a78bfa 100%);
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
            Achievements
        </h1>
        <p style='font-size: 1rem; color: rgba(255,255,255,0.6); font-weight: 500;'>
            Track your progress and unlock rewards
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Get user achievements
    achievements = get_user_achievements(st.session_state.user_id)
    
    # ==========================================
    # PROGRESS OVERVIEW
    # ==========================================
    st.markdown("### Overall Progress")
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        progress = achievements['unlocked_count'] / achievements['total'] if achievements['total'] > 0 else 0
        st.progress(progress)
        st.caption(f"{achievements['unlocked_count']} of {achievements['total']} achievements unlocked")
    
    with col2:
        st.metric("Unlocked", achievements['unlocked_count'])
    
    with col3:
        st.metric("Locked", achievements['total'] - achievements['unlocked_count'])
    
    st.divider()
    
    # ==========================================
    # UNLOCKED ACHIEVEMENTS
    # ==========================================
    if achievements['unlocked']:
        st.markdown("### Unlocked Achievements")
        
        cols = st.columns(3)
        
        for i, achievement in enumerate(achievements['unlocked']):
            with cols[i % 3]:
                st.markdown(f"""
                <div style='
                    background: linear-gradient(135deg, rgba(16, 185, 129, 0.15), rgba(16, 185, 129, 0.05));
                    border: 2px solid {COLORS['success']}40;
                    border-radius: 1rem;
                    padding: 1.5rem;
                    margin-bottom: 1rem;
                    text-align: center;
                '>
                    <div style='font-size: 3rem; margin-bottom: 0.5rem;'>{achievement.get('icon', '🏆')}</div>
                    <h4 style='color: {COLORS['success']}; margin-bottom: 0.5rem; font-size: 1.1rem;'>{achievement['name']}</h4>
                    <p style='font-size: 0.875rem; color: rgba(255,255,255,0.7); margin-bottom: 1rem;'>{achievement['description']}</p>
                    <span style='
                        display: inline-block;
                        background: {COLORS['success']}30;
                        color: {COLORS['success']};
                        padding: 0.25rem 0.75rem;
                        border-radius: 999px;
                        font-size: 0.75rem;
                        font-weight: 700;
                    '>+{achievement['xp_reward']} XP</span>
                </div>
                """, unsafe_allow_html=True)
        
        st.divider()
    else:
        st.info("Complete workouts to unlock your first achievement!")
        st.divider()
    
    # ==========================================
    # LOCKED ACHIEVEMENTS
    # ==========================================
    if achievements['locked']:
        st.markdown("### Locked Achievements")
        st.caption("Complete the requirements to unlock these achievements")
        st.markdown("")
        
        cols = st.columns(3)
        
        for i, achievement in enumerate(achievements['locked']):
            with cols[i % 3]:
                st.markdown(f"""
                <div style='
                    background: linear-gradient(135deg, rgba(100, 116, 139, 0.15), rgba(100, 116, 139, 0.05));
                    border: 2px solid rgba(255,255,255,0.1);
                    border-radius: 1rem;
                    padding: 1.5rem;
                    margin-bottom: 1rem;
                    opacity: 0.6;
                    text-align: center;
                '>
                    <div style='font-size: 3rem; margin-bottom: 0.5rem; filter: grayscale(100%);'>{achievement.get('icon', '🔒')}</div>
                    <h4 style='color: rgba(255,255,255,0.5); margin-bottom: 0.5rem; font-size: 1.1rem;'>{achievement['name']}</h4>
                    <p style='font-size: 0.875rem; color: rgba(255,255,255,0.4); margin-bottom: 1rem;'>{achievement['description']}</p>
                    <span style='
                        display: inline-block;
                        background: rgba(255,255,255,0.1);
                        color: rgba(255,255,255,0.4);
                        padding: 0.25rem 0.75rem;
                        border-radius: 999px;
                        font-size: 0.75rem;
                        font-weight: 700;
                    '>+{achievement['xp_reward']} XP</span>
                </div>
                """, unsafe_allow_html=True)
        
        st.divider()
    
    # ==========================================
    # TIPS SECTION
    # ==========================================
    st.markdown("### Tips for Unlocking Achievements")
    
    tips = [
        "**Stay Consistent**: Many achievements require completing workouts over multiple days",
        "**Try Different Exercises**: Some achievements are exercise-specific",
        "**Aim for Quality**: High-performance scores unlock special achievements",
        "**Join Programs**: Completing training programs unlocks exclusive rewards",
        "**Build Streaks**: Daily workout streaks unlock powerful achievements"
    ]
    
    for tip in tips:
        st.markdown(f"- {tip}")
