"""
History Page - Professional & Organized
Clean design with comprehensive workout statistics
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from backend.services.workout_service import get_user_workouts, get_workout_stats
from src.design_system import COLORS


def set_background(img_b64):
    """Set page background image"""
    if img_b64:
        st.markdown(
            f"""<div class='bg-overlay' style='background-image: url(data:image/png;base64,{img_b64})'></div>""",
            unsafe_allow_html=True
        )


def history_page(background_b64=None):
    """Render the professional workout history page"""
    set_background(background_b64)
    
    # ==========================================
    # HERO SECTION
    # ==========================================
    st.markdown("""
    <div style='text-align: center; padding: 2rem 0 1rem 0; margin-bottom: 2rem; border-bottom: 1px solid rgba(255,255,255,0.1);'>
        <h1 style='font-size: 2.5rem; font-weight: 800; margin-bottom: 0.5rem; 
                   background: linear-gradient(135deg, #ffffff 0%, #a78bfa 100%);
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
            Workout History
        </h1>
        <p style='font-size: 1rem; color: rgba(255,255,255,0.6); font-weight: 500;'>
            View your progress and track your performance over time
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Get user workouts
    workouts = get_user_workouts(st.session_state.user_id, limit=50)
    
    if not workouts:
        st.info("No workout history yet. Start training to build your history!")
        if st.button("Start Workout", use_container_width=True, type="primary"):
            st.session_state.page = 'workout'
            st.rerun()
        return
    
    # Convert to DataFrame
    df = pd.DataFrame([{
        'Date': workout.timestamp.strftime('%Y-%m-%d %H:%M'),
        'Exercise': workout.exercise.title(),
        'Reps': workout.repetitions,
        'Score': workout.score,
        'Duration': workout.duration,
       'Timestamp': workout.timestamp
    } for workout in workouts])
    
    # Get statistics  
    stats = get_workout_stats(st.session_state.user_id, days=30)
    
    # ==========================================
    # STATISTICS SUMMARY
    # ==========================================
    st.markdown("### 30-Day Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    col1.metric("Total Workouts", stats['total_workouts'])
    col2.metric("Average Score", f"{stats['average_score']:.1f}%")
    col3.metric("Best Score", f"{stats['best_score']:.0f}%" if stats['best_score'] else "N/A")
    
    favorite = stats['favorite_exercise'].title() if stats['favorite_exercise'] else "N/A"
    col4.metric("Favorite Exercise", favorite)
    
    st.divider()
    
    # ==========================================
    # PERFORMANCE EVOLUTION
    # ==========================================
    st.markdown("### Performance Evolution")
    
    fig = go.Figure()
    
    # Add score line
    fig.add_trace(go.Scatter(
        x=df['Timestamp'],
        y=df['Score'],
        mode='lines+markers',
        name='Score',
        line=dict(color=COLORS['primary'], width=4),
        marker=dict(size=10, color=COLORS['accent'], line=dict(width=2, color='white'))
    ))
    
    # Add trend line
    if len(df) >= 5:
        df['MA5'] = df['Score'].rolling(window=5).mean()
        fig.add_trace(go.Scatter(
            x=df['Timestamp'],
            y=df['MA5'],
            mode='lines',
            name='Trend (5-workout MA)',
            line=dict(color=COLORS['success'], width=2, dash='dash'),
            opacity=0.7
        ))
    
    fig.update_layout(
        hovermode='x unified',
        template='plotly_dark',
        height=400,
        xaxis_title="Date",
        yaxis_title="Score (%)",
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.divider()
    
    # ==========================================
    # DISTRIBUTIONS
    # ==========================================
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Exercise Distribution")
        exercise_counts = df['Exercise'].value_counts()
        
        fig_pie = go.Figure(data=[go.Pie(
            labels=exercise_counts.index,
            values=exercise_counts.values,
            hole=0.4,
            marker=dict(colors=[COLORS['primary'], COLORS['secondary'], COLORS['accent'], 
                       COLORS['success'], COLORS['info']])
        )])
        
        fig_pie.update_layout(template='plotly_dark', height=300, showlegend=True)
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        st.markdown("### Score Distribution")
        
        fig_hist = go.Figure(data=[go.Histogram(
            x=df['Score'],
            nbinsx=10,
            marker=dict(color=COLORS['primary'], line=dict(color='white', width=1))
        )])
        
        fig_hist.update_layout(
            template='plotly_dark',
            height=300,
            xaxis_title="Score (%)",
            yaxis_title="Count",
            showlegend=False
        )
        
        st.plotly_chart(fig_hist, use_container_width=True)
    
    st.divider()
    
    # ==========================================
    # DETAILED TABLE
    # ==========================================
    st.markdown("### Workout Details")
    
    # Prepare display dataframe
    display_df = df[['Date', 'Exercise', 'Reps', 'Score', 'Duration']].copy()
    display_df['Score'] = display_df['Score'].apply(lambda x: f"{x:.1f}%")
    display_df['Duration'] = display_df['Duration'].apply(lambda x: f"{x}s")
    
    st.dataframe(display_df, use_container_width=True, hide_index=True, height=400)
    
    # Export button
    csv_data = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Export to CSV",
        data=csv_data,
        file_name=f"smartcoach_history_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv",
        use_container_width=True
    )
