"""
Bibliothèque de programmes d'entraînement pour SmartCoach Pro
Programmes pré-définis et personnalisables
"""
from typing import List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
import logging
from sqlalchemy import func

from backend.database import get_db
from backend.models import Program, ProgramExercise, UserProgram, ProgramStatus, FitnessLevel, Workout

logger = logging.getLogger(__name__)


@dataclass
class ExerciseDay:
    """Un exercice dans un jour de programme"""
    exercise: str
    sets: int
    reps: int
    rest_time: int  # seconds
    notes: str = ""


# Programmes pré-définis
PREDEFINED_PROGRAMS = [
    {
        'name': 'Force Foundation - Débutant',
        'description': 'Programme de 4 semaines pour construire les bases de la force',
        'difficulty': FitnessLevel.BEGINNER,
        'duration_weeks': 4,
        'icon': '🌱',
        'schedule': [
            # Semaine 1-4, répété
            [('squat', 3, 8, 60), ('pushup', 3, 10, 60), ('plank', 3, 1, 60)],  # Jour 1
            [],  # Jour 2 - Rest
            [('jumping_jack', 3, 15, 45), ('curl', 3, 10, 60)],  # Jour 3
            [],  # Jour 4 - Rest
            [('squat', 3, 10, 60), ('pushup', 3, 12, 60)],  # Jour 5
            [],  # Jour 6 - Rest
            [],  # Jour 7 - Rest
        ]
    },
    {
        'name': 'Athletic Build - Intermédiaire',
        'description': 'Programme de 8 semaines pour développer force et endurance',
        'difficulty': FitnessLevel.INTERMEDIATE,
        'duration_weeks': 8,
        'icon': '💪',
        'schedule': [
            [('squat', 4, 12, 60), ('pushup', 4, 15, 60), ('curl', 3, 12, 60)],
            [('jumping_jack', 4, 20, 45), ('plank', 4, 1, 60)],
            [],  # Rest
            [('squat', 4, 15, 60), ('pushup', 4, 18, 60), ('curl', 4, 12, 60)],
            [('jumping_jack', 4, 25, 45), ('plank', 4, 1, 60)],
            [],  # Rest
            [],  # Rest
        ]
    },
    {
        'name': 'Peak Performance - Avancé',
        'description': 'Programme intensif de 12 semaines pour athlètes confirmés',
        'difficulty': FitnessLevel.ADVANCED,
        'duration_weeks': 12,
        'icon': '🏆',
        'schedule': [
            [('squat', 5, 15, 45), ('pushup', 5, 20, 45), ('curl', 4, 15, 45), ('plank', 4, 1, 45)],
            [('jumping_jack', 5, 30, 30), ('squat', 4, 20, 45), ('pushup', 4, 25, 45)],
            [('curl', 5, 18, 45), ('plank', 5, 1, 45), ('jumping_jack', 4, 35, 30)],
            [],  # Rest
            [('squat', 5, 20, 45), ('pushup', 5, 25, 45), ('curl', 5, 20, 45)],
            [('jumping_jack', 5, 40, 30), ('plank', 5, 1, 45)],
            [],  # Rest
        ]
    },
    {
        'name': 'Perte de Poids Express',
        'description': 'Programme cardio intensif de 6 semaines',
        'difficulty': FitnessLevel.INTERMEDIATE,
        'duration_weeks': 6,
        'icon': '🔥',
        'schedule': [
            [('jumping_jack', 5, 30, 30), ('squat', 4, 15, 45), ('pushup', 4, 15, 45)],
            [('jumping_jack', 5, 35, 30), ('plank', 4, 1, 45), ('curl', 3, 12, 60)],
            [('jumping_jack', 5, 40, 30), ('squat', 4, 18, 45)],
            [],  # Rest
            [('jumping_jack', 6, 40, 30), ('pushup', 5, 18, 45), ('plank', 4, 1, 45)],
            [],  # Rest
            [],  # Rest
        ]
    },
    {
        'name': 'Gain Musculaire',
        'description': 'Programme hypertrophie de 10 semaines',
        'difficulty': FitnessLevel.ADVANCED,
        'duration_weeks': 10,
        'icon': '💎',
        'schedule': [
            [('squat', 5, 12, 90), ('pushup', 5, 15, 90), ('curl', 5, 12, 90)],
            [],  # Rest
            [('squat', 5, 15, 90), ('pushup', 5, 18, 90), ('plank', 4, 1, 60)],
            [],  # Rest
            [('curl', 6, 15, 90), ('squat', 5, 18, 90), ('pushup', 5, 20, 90)],
            [],  # Rest
            [],  # Rest
        ]
    }
]


def init_predefined_programs():
    """Initialise les programmes pré-définis dans la BDD"""
    db = get_db()
    
    try:
        # Vérifier si déjà initialisé
        existing = db.query(Program).count()
        if existing > 0:
            print(f"📌 {existing} programmes déjà en base")
            return
        
        for prog_data in PREDEFINED_PROGRAMS:
            # Créer le programme
            program = Program(
                name=prog_data['name'],
                description=prog_data['description'],
                difficulty=prog_data['difficulty'],
                duration_weeks=prog_data['duration_weeks'],
                icon=prog_data['icon'],
                created_by='system',
                is_public=True
            )
            db.add(program)
            db.flush()  # Pour obtenir l'ID
            
            # Ajouter les exercices
            schedule= prog_data['schedule']
            for week in range(prog_data['duration_weeks']):
                for day_idx, day_exercises in enumerate(schedule):
                    if not day_exercises:  # Jour de repos
                        continue
                    
                    day_number = (week * 7) + day_idx + 1
                    
                    for order, (exercise, sets, reps, rest) in enumerate(day_exercises):
                        prog_exercise = ProgramExercise(
                            program_id=program.id,
                            day=day_number,
                            exercise=exercise,
                            sets=sets,
                            reps=reps,
                            rest_time=rest,
                            order=order
                        )
                        db.add(prog_exercise)
        
        db.commit()
        print(f"✅ {len(PREDEFINED_PROGRAMS)} programmes initialisés")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Erreur init programmes: {e}")
    finally:
        db.close()


def get_all_programs() -> List[Dict]:
    """Récupère tous les programmes disponibles"""
    db = get_db()
    
    try:
        programs = db.query(Program).filter(Program.is_public == True).all()
        
        return [{
            'id': p.id,
            'name': p.name,
            'description': p.description,
            'difficulty': p.difficulty.value,
            'duration_weeks': p.duration_weeks,
            'icon': p.icon,
            'total_days': p.duration_weeks * 7
        } for p in programs]
        
    finally:
        db.close()


def get_program_details(program_id: int) -> Optional[Dict]:
    """Récupère les détails complets d'un programme"""
    db = get_db()
    
    try:
        program = db.query(Program).filter(Program.id == program_id).first()
        if not program:
            return None
        
        exercises = db.query(ProgramExercise).filter(
            ProgramExercise.program_id == program_id
        ).order_by(ProgramExercise.day, ProgramExercise.order).all()
        
        # Organiser par jour
        days = {}
        for ex in exercises:
            if ex.day not in days:
                days[ex.day] = []
            days[ex.day].append({
                'exercise': ex.exercise,
                'sets': ex.sets,
                'reps': ex.reps,
                'rest_time': ex.rest_time,
                'notes': ex.notes
            })
        
        return {
            'id': program.id,
            'name': program.name,
            'description': program.description,
            'difficulty': program.difficulty.value,
            'duration_weeks': program.duration_weeks,
            'icon': program.icon,
            'days': days
        }
        
    finally:
        db.close()


def enroll_user_in_program(user_id: int, program_id: int) -> bool:
    """Inscrit un utilisateur à un programme"""
    db = get_db()
    
    try:
        # Vérifier si déjà inscrit à un programme actif
        active_program = db.query(UserProgram).filter(
            UserProgram.user_id == user_id,
            UserProgram.status == ProgramStatus.ACTIVE
        ).first()
        
        if active_program:
            # Mettre en pause l'ancien programme
            active_program.status = ProgramStatus.PAUSED
        
        # Créer nouvelle inscription
        user_program = UserProgram(
            user_id=user_id,
            program_id=program_id,
            current_day=1,
            status=ProgramStatus.ACTIVE
        )
        db.add(user_program)
        
        db.commit()
        return True
        
    except Exception as e:
        db.rollback()
        print(f"❌ Erreur enrollment: {e}")
        return False
    finally:
        db.close()


def get_user_active_program(user_id: int) -> Optional[Dict]:
    """Récupère le programme actif avec auto-advance calendrier (SANS RÉCURSION)"""
    db = get_db()
    
    try:
        user_program = db.query(UserProgram).filter(
            UserProgram.user_id == user_id,
            UserProgram.status == ProgramStatus.ACTIVE
        ).first()
        
        if not user_program:
            return None
        
        program = db.query(Program).filter(Program.id == user_program.program_id).first()
        
        if not program:
            return None
        
        # ✅ AUTO-ADVANCE: Avancer UNE SEULE FOIS si nouveau jour calendrier
        today = datetime.utcnow().date()
        start_date = user_program.start_date.date()
        current_day = user_program.current_day
        total_days = program.duration_weeks * 7
        
        # Date attendue pour le jour actuel du programme
        expected_date = start_date + timedelta(days=current_day - 1)
        
        # Si on est APRÈS la date attendue ET qu'on n'a pas déjà avancé aujourd'hui
        if today > expected_date and current_day < total_days:
            # Avancer d'UN SEUL jour
            user_program.current_day += 1
            db.commit()
            logger.info(f"Auto-advanced user {user_id} from day {current_day} to {user_program.current_day}")
            # Mettre à jour current_day pour le reste de la fonction
            current_day = user_program.current_day
            
            # Vérifier si programme terminé
            if current_day >= total_days:
                user_program.status = ProgramStatus.COMPLETED
                user_program.completion_date = datetime.utcnow()
                db.commit()
                logger.info(f"User {user_id} completed program!")
                return None
        
        # Récupérer les exercices du jour actuel (après potentiel avancement)
        today_exercises = db.query(ProgramExercise).filter(
            ProgramExercise.program_id == program.id,
            ProgramExercise.day == user_program.current_day
        ).order_by(ProgramExercise.order).all()
        
        total_days = program.duration_weeks * 7
        progress_percent = (user_program.current_day / total_days) * 100
        
        return {
            'id': user_program.id,
            'program_id': program.id,
            'program_name': program.name,
            'program_icon': program.icon,
            'current_day': user_program.current_day,
            'total_days': total_days,
            'progress_percent': progress_percent,
            'today_exercises': [{
                'exercise': ex.exercise,
                'sets': ex.sets,
                'reps': ex.reps,
                'rest_time': ex.rest_time
            } for ex in today_exercises],
            'is_rest_day': len(today_exercises) == 0
        }
        
    finally:
        db.close()


def advance_program_day(user_id: int) -> bool:
    """
    Valide que tous les exercices du jour sont terminés
    L'avancement réel se fait automatiquement le lendemain dans get_user_active_program()
    
    Returns:
        True si validation réussie, False sinon
    """
    db = get_db()
    
    try:
        user_program = db.query(UserProgram).filter(
            UserProgram.user_id == user_id,
            UserProgram.status == ProgramStatus.ACTIVE
        ).first()
        
        if not user_program:
            return False
        
        # Juste valider - l'avancement se fera automatiquement demain
        logger.info(f"User {user_id} completed day {user_program.current_day}")
        return True
        
    except Exception as e:
        logger.error(f"Error validating day completion for user {user_id}: {e}")
        return False
    finally:
        db.close()
