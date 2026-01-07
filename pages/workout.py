"""
Workout Page - Professional & Organized
Modern design while preserving all AI features
"""

import streamlit as st
import plotly.graph_objects as go
import numpy as np
import logging
from src import SignalGenerator, MovementAnalyzer, ExerciseClassifier, EXERCISES
from backend.services.workout_service import create_workout
from backend.services.ai_coach_service import AICoach
from src.gamification import check_and_unlock_achievements
from src.design_system import COLORS

# Setup logging
logger = logging.getLogger(__name__)


def set_background(img_b64):
    """Set page background image"""
    if img_b64:
        st.markdown(
            f"""<div class='bg-overlay' style='background-image: url(data:image/png;base64,{img_b64})'></div>""",
            unsafe_allow_html=True
        )


@st.cache_resource
def load_classifier():
    """Load the exercise classifier model"""
    try:
        clf = ExerciseClassifier()
        clf.load_model('models/exercise_classifier.pkl')
        logger.info("Exercise classifier loaded successfully")
        return clf
    except FileNotFoundError:
        logger.error("Classifier model not found at models/exercise_classifier.pkl")
        return None
    except Exception as e:
        logger.error(f"Failed to load exercise classifier: {str(e)}")
        return None


def workout_page(background_b64=None):
    """Render the professional workout page"""
    set_background(background_b64)
    
    # ==========================================
    # HERO SECTION - Professional
    # ==========================================
    st.markdown("""
    <div style='text-align: center; padding: 2rem 0 1rem 0; margin-bottom: 2rem; border-bottom: 1px solid rgba(255,255,255,0.1);'>
        <h1 style='font-size: 2.5rem; font-weight: 800; margin-bottom: 0.5rem; 
                   background: linear-gradient(135deg, #ffffff 0%, #a78bfa 100%);
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
            Start Workout
        </h1>
        <p style='font-size: 1rem; color: rgba(255,255,255,0.6); font-weight: 500;'>
            Track your exercise performance with AI-powered analysis
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    coach = AICoach()
    
    # ==========================================
    # EXERCISE SELECTION - Prominent
    # ==========================================
    st.markdown("### Exercise Selection")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        auto_detect = st.checkbox(
            "Enable AI Auto-Detection",
            help="Automatically detect exercise type using machine learning"
        )
        
        if not auto_detect:
            exercise_type = st.selectbox(
                "Choose Exercise",
                list(EXERCISES.keys()),
                format_func=lambda x: f"{EXERCISES[x]['name']}",
                help="Select the exercise you want to perform"
            )
        else:
            st.info("AI will automatically detect your exercise type")
            # Load classifier if not already loaded
            if 'classifier' not in st.session_state or st.session_state.classifier is None:
                st.session_state.classifier = load_classifier()
                if st.session_state.classifier:
                    st.success("AI Model Loaded Successfully")
                else:
                    st.warning("AI Model not available, using random selection")
            
            # Use random exercise for simulation
            exercise_type = np.random.choice(list(EXERCISES.keys()))
    
    with col2:
        st.markdown("")  # Spacing
        st.markdown("")  # Spacing
        if st.button("START WORKOUT", use_container_width=True, type="primary", key="start_workout_btn"):
            st.session_state.workout_started = True
    
    st.divider()
    
    # ==========================================
    # WORKOUT SETTINGS - Collapsible
    # ==========================================
    with st.expander("⚙️ Advanced Settings", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            duration = st.slider(
                "Duration (seconds)",
                min_value=5,
                max_value=20,
                value=10,
                help="Workout duration for signal generation"
            )
        
        with col2:
            sampling_rate = st.slider(
                "Sampling Rate (Hz)",
                min_value=30,
                max_value=100,
                value=50,
                help="Signal sampling frequency"
            )
    
    # ==========================================
    # WORKOUT EXECUTION
    # ==========================================
    if st.session_state.get('workout_started', False):
        with st.spinner("Generating workout data and analyzing..."):
            # Generate exercise signal
            generator = SignalGenerator(duration=duration, sampling_rate=sampling_rate)
            time_data, acc_x, acc_y, acc_z = generator.get_exercise_signal(exercise_type)
            
            predicted_exercise = exercise_type
            confidence = None
            
            # AI Detection if enabled
            if auto_detect and st.session_state.classifier:
                predicted_exercise, confidence, _ = st.session_state.classifier.predict(acc_x, acc_y, acc_z)
                st.success(
                    f"Detected: {EXERCISES[predicted_exercise]['name']} ({confidence:.1%} confidence)"
                )
            
            # Analyze movement
            analyzer = MovementAnalyzer(time_data, acc_x, acc_y, acc_z)
            analysis = analyzer.get_full_analysis(predicted_exercise)
            
            # Generate AI feedback
            feedback = coach.generate_workout_feedback(
                predicted_exercise,
                analysis['score'],
                analysis['regularity'],
                analysis['speed'],
                analysis['repetitions']
            )
        
        st.divider()
        
        # ==========================================
        # RESULTS DISPLAY
        # ==========================================
        st.markdown("### Workout Results")
        
        # Performance Metrics
        col1, col2, col3, col4 = st.columns(4)
        
        col1.metric("Repetitions", analysis['repetitions'])
        col2.metric("Duration", f"{analysis['duration']}s")
        col3.metric("Score", f"{analysis['score']:.1f}%")
        col4.metric("Regularity", f"{analysis['regularity']:.1f}%")
        
        st.divider()
        
        # Signal Visualization
        st.markdown("### Signal Data - 3 Axes")
        
        # Create interactive plot
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=time_data, y=acc_x,
            mode='lines',
            name='X Axis',
            line=dict(color=COLORS['primary'], width=3)
        ))
        fig.add_trace(go.Scatter(
            x=time_data, y=acc_y,
            mode='lines',
            name='Y Axis',
            line=dict(color=COLORS['secondary'], width=3)
        ))
        fig.add_trace(go.Scatter(
            x=time_data, y=acc_z,
            mode='lines',
            name='Z Axis',
            line=dict(color=COLORS['accent'], width=3)
        ))
        
        fig.update_layout(
            height=450,
            template='plotly_dark',
            hovermode='x unified',
            xaxis_title="Time (s)",
            yaxis_title="Acceleration (m/s²)"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.divider()
        
        # AI Feedback
        st.success("Workout Completed Successfully!")
        st.info(f"**Coach Feedback:** {feedback}")
        
        # Save workout to database
        if st.session_state.user_id:
            create_workout(
                st.session_state.user_id,
                predicted_exercise,
                analysis['repetitions'],
                analysis['duration'],
                analysis['score'],
                analysis['regularity'],
                analysis['speed'],
                feedback,
                auto_detect,
                confidence
            )
            
            # Check for new achievements
            newly_unlocked = check_and_unlock_achievements(st.session_state.user_id)
            
            if newly_unlocked:
                st.balloons()
                st.markdown("### New Achievements Unlocked!")
                for achievement in newly_unlocked:
                    st.success(f"**{achievement['name']}** - +{achievement['xp_reward']} XP")
                    st.caption(achievement['description'])
        
        st.divider()
        
        # Reset button
        if st.button("Start Another Workout", use_container_width=True, key="reset_workout"):
            st.session_state.workout_started = False
            st.rerun()
