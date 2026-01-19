"""
Service pour gérer les programmes d'entraînement actifs
"""
from backend.database import get_db
from backend.models import UserProgram, Program, ProgramExercise, ProgramStatus
from sqlalchemy import and_
from typing import Optional
import logging

logger = logging.getLogger(__name__)


def get_active_user_program(user_id: int) -> Optional[UserProgram]:
    """
    Retourne le programme actif de l'utilisateur
    
    Args:
        user_id: ID de l'utilisateur
        
    Returns:
        UserProgram actif ou None
    """
    db = get_db()
    try:
        program = db.query(UserProgram)\
            .filter(
                and_(
                    UserProgram.user_id == user_id,
                    UserProgram.status == ProgramStatus.ACTIVE
                )
            )\
            .first()
        return program
    except Exception as e:
        logger.error(f"Error getting active program: {e}")
        return None
    finally:
        db.close()


def get_program_exercise_for_day(program_id: int, day_number: int) -> Optional[str]:
    """
    Retourne l'exercice recommandé pour un jour spécifique du programme
    
    Args:
        program_id: ID du programme
        day_number: Numéro du jour (1-based)
        
    Returns:
        Type d'exercice ou None
    """
    db = get_db()
    try:
        exercise = db.query(ProgramExercise)\
            .filter(
                and_(
                    ProgramExercise.program_id == program_id,
                    ProgramExercise.day_number == day_number
                )
            )\
            .first()
        
        return exercise.exercise_type if exercise else None
    except Exception as e:
        logger.error(f"Error getting program exercise: {e}")
        return None
    finally:
        db.close()


def increment_program_day(user_program_id: int) -> bool:
    """
    Incrémente le compteur de jours complétés du programme
    
    Args:
        user_program_id: ID du UserProgram
        
    Returns:
        True si succès, False sinon
    """
    db = get_db()
    try:
        program = db.query(UserProgram).get(user_program_id)
        if program and program.status == ProgramStatus.ACTIVE:
            program.days_completed += 1
            
            # Vérifier si programme terminé
            total_days = program.program.duration_weeks * 7
            if program.days_completed >= total_days:
                program.status = ProgramStatus.COMPLETED
                logger.info(f"Program {program.program.name} completed for user {program.user_id}")
            
            db.commit()
            return True
        return False
    except Exception as e:
        logger.error(f"Error incrementing program day: {e}")
        db.rollback()
        return False
    finally:
        db.close()


def get_program_progress(user_program: UserProgram) -> dict:
    """
    Retourne les informations de progression d'un programme
    
    Args:
        user_program: Instance UserProgram
        
    Returns:
        Dict avec current_day, total_days, percentage
    """
    if not user_program or not user_program.program:
        return None
    
    total_days = user_program.program.duration_weeks * 7
    current_day = user_program.days_completed + 1
    percentage = min(100, (user_program.days_completed / total_days) * 100)
    
    return {
        'current_day': current_day,
        'total_days': total_days,
        'percentage': percentage,
        'program_name': user_program.program.name
    }
