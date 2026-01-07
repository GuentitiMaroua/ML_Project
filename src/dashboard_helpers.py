"""
Dashboard Helper Functions
Optimized data fetching for better performance
"""
from typing import Dict, Any
from backend.database import get_db
from backend.models import UserStats, User
from src.gamification import get_level_info, get_user_achievements
from src.workout_programs import get_user_active_program


def get_dashboard_data(user: User) -> Dict[str, Any]:
    """
    Get all dashboard data in a single optimized call
    
    Args:
        user: User object
        
    Returns:
        Dictionary with all dashboard data
    """
    db = get_db()
    
    try:
        # Get user stats
        stats = db.query(UserStats).filter(UserStats.user_id == user.id).first()
        if not stats:
            stats = UserStats(user_id=user.id)
            db.add(stats)
            db.commit()
            db.refresh(stats)
        
        # Get level info
        level_info = get_level_info(stats.xp_points)
        
        # Get achievements
        achievements = get_user_achievements(user.id)
        
        # Get active program
        active_program = get_user_active_program(user.id)
        
        return {
            'user': user,
            'stats': stats,
            'level': level_info,
            'achievements': achievements,
            'active_program': active_program
        }
    finally:
        db.close()


def format_number(num: int) -> str:
    """Format large numbers with K/M suffix"""
    if num >= 1000000:
        return f"{num/1000000:.1f}M"
    elif num >= 1000:
        return f"{num/1000:.1f}K"
    return str(num)
