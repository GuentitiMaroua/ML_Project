"""
My Program Page - Daily Workout Tracking
Shows detailed workout plan for current day with progress tracking
"""

import streamlit as st
from src.workout_programs import get_user_active_program, advance_program_day
from src.design_system import COLORS
from datetime import datetime


def get_exercise_emoji(exercise: str) -> str:
    """Get emoji for exercise type - Removed for professional design"""
    return ""


def format_exercise_name(exercise: str) -> str:
    """Format exercise name for display"""
    name_map = {
        'squat': 'Squat',
        'pushup': 'Push-up',
        'curl': 'Bicep Curl',
        'jumping_jack': 'Jumping Jack',
        'plank': 'Plank Hold',
        'bench_press': 'Bench Press',
        'deadlift': 'Deadlift'
    }
    return name_map.get(exercise.lower(), exercise.capitalize())


def my_program_page():
    """Render the My Program page with daily workout details"""
    
    # Get active program (avec auto-advance calendrier intégré)
    program = get_user_active_program(st.session_state.user_id)
    
    if not program:
        # ==========================================
        # NO ACTIVE PROGRAM
        # ==========================================
        st.markdown("""
        <div style='text-align: center; padding: 4rem 2rem;'>
            <h2 style='color: rgba(255,255,255,0.9); margin-bottom: 1rem;'>No Active Program</h2>
            <p style='color: rgba(255,255,255,0.6); font-size: 1.1rem; margin-bottom: 2rem;'>
                You're not currently enrolled in a training program.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Browse Programs", type="primary", use_container_width=True):
            st.session_state.page = 'programs'
            st.rerun()
        
        return
    
    # ==========================================
    # HEADER SECTION
    # ==========================================
    st.markdown(f"""
    <div style='text-align: center; padding: 2rem 0 1rem 0; border-bottom: 1px solid rgba(255,255,255,0.1);'>
        <h1 style='font-size: 2.5rem; font-weight: 800; margin-bottom: 0.5rem; 
                   background: linear-gradient(135deg, #ffffff 0%, #a78bfa 100%);
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
            {program['program_name']}
        </h1>
        <p style='font-size: 1.2rem; color: rgba(255,255,255,0.7); font-weight: 500;'>
            Day {program['current_day']} of {program['total_days']}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # ==========================================
    # PROGRESS BAR
    # ==========================================
    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        st.metric("Current Day", program['current_day'])
    
    with col2:
        progress = program['progress_percent']
        st.progress(progress / 100)
        st.caption(f"Progress: {progress:.1f}%")
    
    with col3:
        remaining = program['total_days'] - program['current_day']
        st.metric("Days Remaining", remaining)
    
    st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
    
    # ==========================================
    # TODAY'S WORKOUT SECTION
    # ==========================================
    st.markdown(f"""
    <div style='margin-bottom: 1.5rem;'>
        <h2 style='font-size: 2rem; font-weight: 700; margin-bottom: 0.5rem;'>
            Today's Workout
        </h2>
        <p style='color: rgba(255,255,255,0.6); font-size: 0.95rem;'>
            {datetime.now().strftime('%A, %B %d, %Y')}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # ==========================================
    # REST DAY OR WORKOUT DAY
    # ==========================================
    if program['is_rest_day']:
        # REST DAY
        st.markdown("""
        <div style='
            background: linear-gradient(135deg, rgba(16, 185, 129, 0.1), rgba(5, 150, 105, 0.05));
            border: 2px solid rgba(16, 185, 129, 0.3);
            border-radius: 1rem;
            padding: 2rem;
            text-align: center;
            margin-bottom: 2rem;
        '>
            <h3 style='font-size: 1.8rem; font-weight: 700; margin-bottom: 0.5rem; color: #10b981;'>
                Rest & Recovery Day
            </h3>
            <p style='color: rgba(255,255,255,0.7); font-size: 1.1rem; line-height: 1.6;'>
                Your body needs time to recover and rebuild. Take it easy today!
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Rest day tips
        st.markdown("### Rest Day Tips")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div style='
                background: linear-gradient(135deg, rgba(99, 102, 241, 0.1), rgba(139, 92, 246, 0.05));
                border-left: 4px solid #6366f1;
                border-radius: 0.75rem;
                padding: 1.5rem;
                margin-bottom: 1rem;
            '>
                <h4 style='color: #a78bfa; margin-bottom: 0.5rem;'>Light Activity</h4>
                <ul style='color: rgba(255,255,255,0.8); line-height: 1.8; margin: 0;'>
                    <li>Gentle stretching</li>
                    <li>Light walking</li>
                    <li>Yoga or meditation</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style='
                background: linear-gradient(135deg, rgba(99, 102, 241, 0.1), rgba(139, 92, 246, 0.05));
                border-left: 4px solid #6366f1;
                border-radius: 0.75rem;
                padding: 1.5rem;
                margin-bottom: 1rem;
            '>
                <h4 style='color: #a78bfa; margin-bottom: 0.5rem;'>Recovery Focus</h4>
                <ul style='color: rgba(255,255,255,0.8); line-height: 1.8; margin: 0;'>
                    <li>Proper hydration</li>
                    <li>Quality sleep (8+ hours)</li>
                    <li>Balanced nutrition</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
    
    else:
        # WORKOUT DAY
        total_exercises = len(program['today_exercises'])
        
        st.markdown(f"""
        <div style='
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.15), rgba(139, 92, 246, 0.1));
            border: 2px solid rgba(99, 102, 241, 0.3);
            border-radius: 1rem;
            padding: 1.5rem;
            margin-bottom: 2rem;
        '>
            <div style='display: flex; justify-content: space-between; align-items: center;'>
                <div>
                    <h3 style='font-size: 1.5rem; font-weight: 700; margin-bottom: 0.3rem;'>
                        {total_exercises} Exercise{'s' if total_exercises > 1 else ''}
                    </h3>
                    <p style='color: rgba(255,255,255,0.7); margin: 0;'>
                        Complete all exercises to finish today's workout
                    </p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Display each exercise
        for idx, exercise in enumerate(program['today_exercises'], 1):
            name = format_exercise_name(exercise['exercise'])
            
            st.markdown(f"""
            <div style='
                background: linear-gradient(135deg, rgba(139, 92, 246, 0.1), rgba(99, 102, 241, 0.05));
                border: 1px solid rgba(139, 92, 246, 0.2);
                border-radius: 1rem;
                padding: 1.5rem;
                margin-bottom: 1rem;
            '>
                <div style='display: flex; align-items: center; margin-bottom: 1rem;'>
                    <div style='
                        background: linear-gradient(135deg, #8b5cf6, #6366f1);
                        width: 2.5rem;
                        height: 2.5rem;
                        border-radius: 50%;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        font-weight: 700;
                        margin-right: 1rem;
                    '>{idx}</div>
                    <div>
                        <h3 style='font-size: 1.4rem; font-weight: 700; margin: 0;'>
                            {name}
                        </h3>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # Exercise details
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Sets", exercise['sets'], help="Number of sets to complete")
            
            with col2:
                reps_label = "Duration" if exercise['exercise'].lower() == 'plank' else "Reps"
                reps_value = f"{exercise['reps']} min" if exercise['exercise'].lower() == 'plank' else exercise['reps']
                st.metric(reps_label, reps_value, help="Repetitions per set")
            
            with col3:
                st.metric("Rest", f"{exercise['rest_time']}s", help="Rest time between sets")
            
            # ✅ Completion checkbox - AUTO-SYNC avec workouts faits AUJOURD'HUI
            from backend.models import Workout
            from sqlalchemy import func
            from backend.database import get_db
            
            # Vérifier si cet exercice a été fait aujourd'hui (calendrier)
            db = get_db()
            workout_done = None
            try:
                today = datetime.now().date()
                workout_done = db.query(Workout).filter(
                    Workout.user_id == st.session_state.user_id,
                    Workout.exercise == exercise['exercise'],
                    func.date(Workout.timestamp) == today
                ).first()
            finally:
                db.close()
            
            # Checkbox auto-cochée ET désactivée si déjà fait
            is_completed = bool(workout_done) or st.session_state.get(f"completed_{idx}", False)
            
            st.checkbox(
                f"Completed {name}" + (" (Done today)" if workout_done else ""),
                key=f"completed_{idx}",
                value=is_completed,
                disabled=bool(workout_done),  # Immutable si déjà fait
                help=f"{'This exercise was completed today' if workout_done else 'Mark this exercise as completed'}"
            )
            
            st.markdown("</div>", unsafe_allow_html=True)
    
    # ==========================================
    # ACTION BUTTONS
    # ==========================================
    st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("Start Workout", type="primary", use_container_width=True):
            st.session_state.page = 'workout'
            st.rerun()
    
    with col2:
        # ✅ VALIDATION: Check if all exercises are ACTUALLY completed in DB
        can_advance = False
        
        if program['is_rest_day']:
            # Rest days can always advance
            can_advance = True
        else:
            # ✅ NOUVELLE LOGIQUE: Vérifier dans la DB si tous les exercices sont faits
            from backend.models import Workout
            from sqlalchemy import func
            from backend.database import get_db
            
            total_exercises = len(program['today_exercises'])
            completed_count = 0
            
            db = get_db()
            try:
                today = datetime.now().date()
                for exercise in program['today_exercises']:
                    # Vérifier si cet exercice a été fait aujourd'hui
                    workout_done = db.query(Workout).filter(
                        Workout.user_id == st.session_state.user_id,
                        Workout.exercise == exercise['exercise'],
                        func.date(Workout.timestamp) == today
                    ).first()
                    
                    if workout_done:
                        completed_count += 1
            finally:
                db.close()
            
            can_advance = (completed_count == total_exercises)
        
        # Show completion status
        if not program['is_rest_day'] and not can_advance:
            # Recalculate for display
            from backend.models import Workout
            from sqlalchemy import func
            from backend.database import get_db
            
            total_exercises = len(program['today_exercises'])
            completed_count = 0
            
            db = get_db()
            try:
                today = datetime.now().date()
                for exercise in program['today_exercises']:
                    workout_done = db.query(Workout).filter(
                        Workout.user_id == st.session_state.user_id,
                        Workout.exercise == exercise['exercise'],
                        func.date(Workout.timestamp) == today
                    ).first()
                    if workout_done:
                        completed_count += 1
            finally:
                db.close()
            
            st.caption(f"Complete all exercises ({completed_count}/{total_exercises})")
            
            # Debug info
            if completed_count < total_exercises:
                st.info(f"**Debug**: You need to complete **{total_exercises - completed_count} more exercise(s) TODAY** to advance.")
        
        if st.button(
            "Complete Day & Advance" if not program['is_rest_day'] else "Next Day",
            type="secondary",
            use_container_width=True,
            disabled=not can_advance
        ):
            if advance_program_day(st.session_state.user_id):
                st.success("Day completed! Great work!")
                st.info("Your next workout day will be available tomorrow. Come back then!")
                
                # Reset checkboxes pour le prochain affichage
                for key in list(st.session_state.keys()):
                    if key.startswith('completed_'):
                        del st.session_state[key]
                
                # ✅ PAS de st.rerun() - Laisser l'utilisateur voir le message
                # La page se rechargera naturellement au prochain refresh
            else:
                st.error("Unable to validate completion. Please try again.")
    
    # ==========================================
    # PROGRAM OVERVIEW
    # ==========================================
    st.markdown("<div style='height: 3rem;'></div>", unsafe_allow_html=True)
    st.markdown("---")
    
    with st.expander("Program Overview & Statistics"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Progress")
            st.metric("Weeks Completed", f"{(program['current_day'] - 1) // 7}")
            st.metric("Days Completed", program['current_day'] - 1)
            st.metric("Completion Rate", f"{program['progress_percent']:.1f}%")
        
        with col2:
            st.markdown("### Remaining")
            remaining_weeks = (program['total_days'] - program['current_day']) // 7
            st.metric("Weeks Left", remaining_weeks)
            st.metric("Days Left", program['total_days'] - program['current_day'])
            
            estimated_finish = datetime.now()
            # Add remaining days
            from datetime import timedelta
            estimated_finish += timedelta(days=program['total_days'] - program['current_day'])
            st.metric("Est. Completion", estimated_finish.strftime("%b %d, %Y"))
