"""
Services pour la gestion des workouts
"""
from typing import List, Optional, Dict
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import Workout, User, UserStats
import pandas as pd
import logging

logger = logging.getLogger(__name__)


def create_workout(
    user_id: int,
    exercise: str,
    repetitions: int,
    duration: float,
    score: float,
    regularity: float,
    speed: float,
    feedback: str,
    detected_by_ai: bool = False,
    ai_confidence: Optional[float] = None,
    notes: Optional[str] = None
) -> Workout:
    """Enregistre un nouveau workout"""
    db = get_db()
    
    try:
        workout = Workout(
            user_id=user_id,
            exercise=exercise,
            repetitions=repetitions,
            duration=duration,
            score=score,
            regularity=regularity,
            speed=speed,
            feedback=feedback,
            detected_by_ai=detected_by_ai,
            ai_confidence=ai_confidence,
            notes=notes,
            timestamp=datetime.utcnow()
        )
        
        db.add(workout)
        update_user_stats_after_workout(db, user_id, duration, score)
        db.commit()
        db.refresh(workout)
        return workout
        
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


def update_user_stats_after_workout(db: Session, user_id: int, duration: float, score: float):
    """Met à jour les stats après workout"""
    stats = db.query(UserStats).filter(UserStats.user_id == user_id).first()
    
    if not stats:
        stats = UserStats(user_id=user_id)
        db.add(stats)
    
    stats.total_workouts += 1
    stats.total_time += duration
    stats.xp_points += calculate_xp_from_score(score)
    stats.level = (stats.xp_points // 100) + 1  # XP_PER_LEVEL = 100
    
    # ✅ Improved Streak Calculation Logic
    today = datetime.utcnow().date()
    
    if stats.last_workout_date:
        last_date = stats.last_workout_date.date()
        diff = (today - last_date).days
        
        if diff == 0:
            # Multiple workouts same day - streak stays the same
            logger.debug(f"Same day workout for user {user_id}, streak unchanged: {stats.current_streak}")
            pass
        elif diff == 1:
            # Consecutive day - increment streak
            stats.current_streak += 1
            stats.best_streak = max(stats.best_streak, stats.current_streak)
            logger.info(f"User {user_id} streak increased to {stats.current_streak} days")
        else:
            # Streak broken - reset to 1
            logger.info(f"User {user_id} streak broken (gap of {diff} days), resetting to 1")
            stats.current_streak = 1
    else:
        # First workout ever
        stats.current_streak = 1
        stats.best_streak = 1
        logger.info(f"First workout for user {user_id}, streak initialized to 1")
    
    stats.last_workout_date = datetime.utcnow()


def calculate_xp_from_score(score: float) -> int:
    """
    Calcule XP selon score
    
    Args:
        score: Score de performance (0-100)
        
    Returns:
        Points XP à attribuer
    """
    if score >= 90:
        return 100  # Excellent
    elif score >= 75:
        return 70   # Good
    elif score >= 60:
        return 50   # Fair
    else:
        return 30   # Basic


def get_user_workouts(
    user_id: int,
    limit: Optional[int] = None,
    exercise: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
) -> List[Workout]:
    """Récupère workouts avec filtres"""
    db = get_db()
    
    try:
        query = db.query(Workout).filter(Workout.user_id == user_id)
        
        if exercise:
            query = query.filter(Workout.exercise == exercise)
        if start_date:
            query = query.filter(Workout.timestamp >= start_date)
        if end_date:
            query = query.filter(Workout.timestamp <= end_date)
        
        query = query.order_by(Workout.timestamp.desc())
        
        if limit:
            query = query.limit(limit)
        
        return query.all()
    finally:
        db.close()


def get_workout_stats(user_id: int, days: int = 30) -> Dict:
    """Stats workouts sur période"""
    db = get_db()
    
    try:
        start_date = datetime.utcnow() - timedelta(days=days)
        workouts = db.query(Workout).filter(
            Workout.user_id == user_id,
            Workout.timestamp >= start_date
        ).all()
        
        if not workouts:
            return {
                'total_workouts': 0,
                'total_time': 0,
                'average_score': 0,
                'best_score': 0,
                'favorite_exercise': None
            }
        
        df = pd.DataFrame([{
            'exercise': w.exercise,
            'score': w.score,
            'duration': w.duration
        } for w in workouts])
        
        return {
            'total_workouts': len(workouts),
            'total_time': df['duration'].sum(),
            'average_score': df['score'].mean(),
            'best_score': df['score'].max(),
            'favorite_exercise': df['exercise'].mode()[0] if len(df) > 0 else None
        }
    finally:
        db.close()


def delete_workout(workout_id: int, user_id: int) -> bool:
    """Supprime workout"""
    db = get_db()
    
    try:
        workout = db.query(Workout).filter(
            Workout.id == workout_id,
            Workout.user_id == user_id
        ).first()
        
        if not workout:
            logger.warning(f"Workout {workout_id} not found for user {user_id}")
            return False
        
        db.delete(workout)
        db.commit()
        logger.info(f"Workout {workout_id} deleted successfully")
        return True
    except Exception as e:
        logger.error(f"Error deleting workout {workout_id}: {str(e)}")
        db.rollback()
        return False
    finally:
        db.close()
