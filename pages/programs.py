"""
Programs Page - Professional & Organized
Modern design with filtering and better UX
"""

import streamlit as st
from src.workout_programs import get_all_programs, enroll_user_in_program, get_user_active_program
from src.design_system import COLORS


def set_background(img_b64):
    """Set page background image"""
    if img_b64:
        st.markdown(
            f"""<div class='bg-overlay' style='background-image: url(data:image/png;base64,{img_b64})'></div>""",
            unsafe_allow_html=True
        )


def get_difficulty_color(difficulty: str) -> str:
    """Get color based on difficulty level"""
    difficulty_colors = {
        'beginner': COLORS['success'],
        'intermediate': COLORS['warning'],
        'advanced': COLORS['danger'],
        'expert': COLORS['accent']
    }
    return difficulty_colors.get(difficulty.lower(), COLORS['info'])


def programs_page(background_b64=None):
    """Render the professional training programs page"""
    set_background(background_b64)
    
    # ==========================================
    # HERO SECTION
    # ==========================================
    st.markdown("""
    <div style='text-align: center; padding: 2rem 0 1rem 0; margin-bottom: 2rem; border-bottom: 1px solid rgba(255,255,255,0.1);'>
        <h1 style='font-size: 2.5rem; font-weight: 800; margin-bottom: 0.5rem; 
                   background: linear-gradient(135deg, #ffffff 0%, #a78bfa 100%);
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
            Training Programs
        </h1>
        <p style='font-size: 1rem; color: rgba(255,255,255,0.6); font-weight: 500;'>
            Structured programs to help you reach your fitness goals
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Get data
    programs = get_all_programs()
    active_program = get_user_active_program(st.session_state.user_id)
    
    # ==========================================
    # ACTIVE PROGRAM DISPLAY
    # ==========================================
    if active_program:
        st.markdown("### Currently Enrolled")
        
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.markdown(f"**{active_program['program_name']}**")
        
        with col2:
            st.metric("Day", f"{active_program['current_day']}/{active_program['total_days']}")
        
        with col3:
            progress = (active_program['current_day'] / active_program['total_days']) * 100
            st.metric("Progress", f"{progress:.0f}%")
        
        st.progress(progress / 100)
        st.divider()
    else:
        st.info("Not currently enrolled in any program. Choose one below to get started!")
        st.divider()
    
    # ==========================================
    # FILTERS & SORTING
    # ==========================================
    st.markdown("### Available Programs")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        difficulty_filter = st.multiselect(
            "Filter by Difficulty",
            options=["Beginner", "Intermediate", "Advanced", "Expert"],
            default=[],
            help="Select difficulty levels to filter programs"
        )
    
    with col2:
        sort_by = st.selectbox(
            "Sort by",
            options=["Name", "Difficulty", "Duration"],
            help="Sort programs by selected criteria"
        )
    
    st.markdown("")
    
    # ==========================================
    # FILTER & SORT PROGRAMS
    # ==========================================
    if not programs:
        st.info("No programs available at this time.")
        return
    
    # Apply difficulty filter
    filtered_programs = programs
    if difficulty_filter:
        filtered_programs = [
            p for p in programs 
            if p['difficulty'].title() in difficulty_filter
        ]
    
    # Apply sorting
    if sort_by == "Name":
        filtered_programs = sorted(filtered_programs, key=lambda x: x['name'])
    elif sort_by == "Difficulty":
        difficulty_order = {'beginner': 1, 'intermediate': 2, 'advanced': 3, 'expert': 4}
        filtered_programs = sorted(
            filtered_programs,
            key=lambda x: difficulty_order.get(x['difficulty'].lower(), 5)
        )
    elif sort_by == "Duration":
        filtered_programs = sorted(filtered_programs, key=lambda x: x['duration_weeks'])
    
    # Show count
    st.caption(f"Showing {len(filtered_programs)} program(s)")
    st.markdown("")
    
    # ==========================================
    # PROGRAMS GRID
    # ==========================================
    if not filtered_programs:
        st.warning("No programs match your selected filters.")
        return
    
    for i in range(0, len(filtered_programs), 2):
        cols = st.columns(2)
        
        for j, col in enumerate(cols):
            idx = i + j
            if idx >= len(filtered_programs):
                break
            
            program = filtered_programs[idx]
            
            with col:
                # Program header
                col_title, col_badge = st.columns([3, 1])
                
                with col_title:
                    st.markdown(f"**{program['name']}**")
                
                with col_badge:
                    difficulty_color = get_difficulty_color(program['difficulty'])
                    st.markdown(f"""
                    <div style='text-align: right;'>
                        <span style='
                            display: inline-block;
                            background: {difficulty_color}20;
                            color: {difficulty_color};
                            padding: 0.25rem 0.75rem;
                            border-radius: 999px;
                            font-size: 0.7rem;
                            font-weight: 700;
                            text-transform: uppercase;
                        '>{program['difficulty']}</span>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Description
                st.caption(program['description'])
                
                # Details
                detail_col1, detail_col2 = st.columns(2)
                with detail_col1:
                    st.caption(f"⏱️ {program['duration_weeks']} weeks")
                with detail_col2:
                    st.caption(f"📊 {program['difficulty'].title()}")
                
                st.markdown("")
                
                # Enrollment button
                is_active = active_program and active_program['program_id'] == program['id']
                
                if is_active:
                    st.success("Currently Enrolled")
                else:
                    if st.button(
                        "Enroll in Program",
                        key=f"enroll_{program['id']}",
                        use_container_width=True
                    ):
                        enroll_user_in_program(st.session_state.user_id, program['id'])
                        st.success(f"Successfully enrolled in {program['name']}!")
                        st.rerun()
                
                st.divider()
    
    # ==========================================
    # INFORMATION SECTION
    # ==========================================
    st.markdown("### About Training Programs")
    
    st.write("""
    Training programs provide structured workout plans to help you achieve specific fitness goals:
    
    - **Beginner**: Perfect for those just starting their fitness journey
    - **Intermediate**: For those with some experience looking to level up
    - **Advanced**: Challenging programs for experienced athletes
    - **Expert**: Elite-level training for maximum performance
    
    Each program guides you day-by-day with recommended exercises, target reps, and progressive difficulty.
    """)
