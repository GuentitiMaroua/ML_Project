"""
Système de gamification pour SmartCoach Pro
Gestion XP, niveaux, badges et achievements
"""
from typing import List, Dict, Optional, Tuple
from datetime import datetime, timedelta
from backend.database import get_db
from backend.models import Achievement, UserAchievement, UserStats, Workout, Notification, NotificationType


# Configuration des niveaux
XP_PER_LEVEL = 100
MAX_LEVEL = 50

# Définition des achievements
ACHIEVEMENTS_DATABASE = [
    {
        'code': 'first_step',
        'name': 'Premier Pas',
        'description': 'Complétez votre premier workout',
        'icon': '🏆',
        'xp_reward': 50,
        'check_func': lambda stats, workouts: stats.total_workouts >= 1
    },
    {
        'code': 'on_fire',
        'name': 'En Feu!',
        'description': '7 jours consécutifs d\'entraînement',
        'icon': '🔥',
        'xp_reward': 200,
        'check_func': lambda stats, workouts: stats.current_streak >= 7
    },
    {
        'code': 'perfect_week',
        'name': 'Semaine Parfaite',
        'description': '7 workouts en une semaine',
        'icon': '⭐',
        'xp_reward': 150,
        'check_func': lambda stats, workouts: count_workouts_last_n_days(workouts, 7) >= 7
    },
    {
        'code': 'century',
        'name': 'Le Centenaire',
        'description': '100 workouts complétés',
        'icon': '💯',
        'xp_reward': 500,
        'check_func': lambda stats, workouts: stats.total_workouts >= 100
    },
    {
        'code': 'speed_demon',
        'name': 'Démon de Vitesse',
        'description': '20 workouts en un mois',
        'icon': '⚡',
        'xp_reward': 250,
        'check_func': lambda stats, workouts: count_workouts_last_n_days(workouts, 30) >= 20
    },
    {
        'code': 'perfectionist',
        'name': 'Perfectionniste',
        'description': 'Score >95% sur 10 workouts',
        'icon': '🎯',
        'xp_reward': 300,
        'check_func': lambda stats, workouts: count_perfect_workouts(workouts) >= 10
    },
    {
        'code': 'iron_will',
        'name': 'Volonté de Fer',
        'description': '30 jours consécutifs',
        'icon': '🦾',
        'xp_reward': 500,
        'check_func': lambda stats, workouts: stats.current_streak >= 30
    },
    {
        'code': 'dedicated',
        'name': 'Dévoué',
        'description': '50 workouts complétés',
        'icon': '💪',
        'xp_reward': 250,
        'check_func': lambda stats, workouts: stats.total_workouts >= 50
    },
    {
        'code': 'marathon',
        'name': 'Marathonien',
        'description': '10 heures d\'entraînement total',
        'icon': '🏃',
        'xp_reward': 350,
        'check_func': lambda stats, workouts: stats.total_time >= 36000  # 10 hours in seconds
    },
    {
        'code': 'rising_star',
        'name': 'Étoile Montante',
        'description': 'Atteindre le niveau 10',
        'icon': '🌟',
        'xp_reward': 200,
        'check_func': lambda stats, workouts: stats.level >= 10
    },
    {
        'code': 'elite_athlete',
        'name': 'Athlète Élite',
        'description': 'Atteindre le niveau 25',
        'icon': '👑',
        'xp_reward': 500,
        'check_func': lambda stats, workouts: stats.level >= 25
    },
    {
        'code': 'legend',
        'name': 'Légende',
        'description': 'Atteindre le niveau 50',
        'icon': '🏅',
        'xp_reward': 1000,
        'check_func': lambda stats, workouts: stats.level >= 50
    },
    {
        'code': 'early_bird',
        'name': 'Lève-tôt',
        'description': '10 workouts avant 8h du matin',
        'icon': '🌅',
        'xp_reward': 150,
        'check_func': lambda stats, workouts: count_workouts_in_time_range(workouts, 0, 8) >= 10
    },
    {
        'code': 'night_owl',
        'name': 'Oiseau de Nuit',
        'description': '10 workouts après 22h',
        'icon': '🌙',
        'xp_reward': 150,
        'check_func': lambda stats, workouts: count_workouts_in_time_range(workouts, 22, 24) >= 10
    },
    {
        'code': 'variety_lover',
        'name': 'Amateur de Variété',
        'description': 'Complétez tous les types d\'exercices',
        'icon': '🎨',
        'xp_reward': 200,
        'check_func': lambda stats, workouts: check_all_exercises_done(workouts)
    }
]


# Helper functions
def count_workouts_last_n_days(workouts: List[Workout], days: int) -> int:
    """Compte les workouts des N derniers jours"""
    cutoff = datetime.utcnow() - timedelta(days=days)
    return sum(1 for w in workouts if w.timestamp >= cutoff)


def count_perfect_workouts(workouts: List[Workout], threshold: float = 95.0) -> int:
    """Compte les workouts avec score > threshold"""
    return sum(1 for w in workouts if w.score >= threshold)


def count_workouts_in_time_range(workouts: List[Workout], start_hour: int, end_hour: int) -> int:
    """Compte les workouts dans une plage horaire"""
    count = 0
    for w in workouts:
        hour = w.timestamp.hour
        if start_hour <= hour < end_hour:
            count += 1
    return count


def check_all_exercises_done(workouts: List[Workout]) -> bool:
    """Vérifie si tous les types d'exercices ont été faits"""
    required_exercises = {'squat', 'pushup', 'curl', 'jumping_jack', 'plank'}
    done_exercises = set(w.exercise for w in workouts)
    return required_exercises.issubset(done_exercises)


def init_achievements():
    """Initialise la table des achievements dans la BDD"""
    db = get_db()
    
    try:
        # Vérifier si déjà initialisé
        existing = db.query(Achievement).count()
        if existing > 0:
            print(f"📌 {existing} achievements déjà en base")
            return
        
        # Créer tous les achievements
        for ach_data in ACHIEVEMENTS_DATABASE:
            achievement = Achievement(
                code=ach_data['code'],
                name=ach_data['name'],
                description=ach_data['description'],
                icon=ach_data['icon'],
                xp_reward=ach_data['xp_reward']
            )
            db.add(achievement)
        
        db.commit()
        print(f"✅ {len(ACHIEVEMENTS_DATABASE)} achievements initialisés")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Erreur init achievements: {e}")
    finally:
        db.close()


def check_and_unlock_achievements(user_id: int) -> List[Dict]:
    """
    Vérifie et débloque les nouveaux achievements pour un utilisateur
    
    Returns:
        Liste des achievements nouvellement débloqués (as dicts)
    """
    db = get_db()
    newly_unlocked = []
    
    try:
        # Récupérer les stats et workouts de l'utilisateur
        stats = db.query(UserStats).filter(UserStats.user_id == user_id).first()
        if not stats:
            return []
        
        workouts = db.query(Workout).filter(Workout.user_id == user_id).all()
        
        # Récupérer les achievements déjà débloqués
        unlocked_ids = set(
            ua.achievement_id 
            for ua in db.query(UserAchievement).filter(UserAchievement.user_id == user_id).all()
        )
        
        # Vérifier chaque achievement
        all_achievements = db.query(Achievement).all()
        
        for achievement in all_achievements:
            # Déjà débloqué? Skip
            if achievement.id in unlocked_ids:
                continue
            
            # Trouver la fonction de check
            ach_def = next((a for a in ACHIEVEMENTS_DATABASE if a['code'] == achievement.code), None)
            if not ach_def:
                continue
            
            # Vérifier la condition
            if ach_def['check_func'](stats, workouts):
                # Débloquer!
                user_achievement = UserAchievement(
                    user_id=user_id,
                    achievement_id=achievement.id,
                    unlocked_at=datetime.utcnow()
                )
                db.add(user_achievement)
                
                # Ajouter XP
                stats.xp_points += achievement.xp_reward
                stats.level = (stats.xp_points // XP_PER_LEVEL) + 1
                
                # Créer notification
                notification = Notification(
                    user_id=user_id,
                    type=NotificationType.ACHIEVEMENT,
                    message=f"Achievement débloqué: {achievement.name} (+{achievement.xp_reward} XP)",
                    is_read=False
                )
                db.add(notification)
                
                # Ajouter au résultat comme dict (pas l'objet Achievement)
                newly_unlocked.append({
                    'id': achievement.id,
                    'code': achievement.code,
                    'name': achievement.name,
                    'description': achievement.description,
                    'icon': achievement.icon,
                    'xp_reward': achievement.xp_reward
                })
        
        db.commit()
        
    except Exception as e:
        db.rollback()
        print(f"Erreur check achievements: {e}")
    finally:
        db.close()
    
    return newly_unlocked


def get_user_achievements(user_id: int) -> Dict:
    """
    Récupère tous les achievements (débloqués et verrouillés)
    
    Returns:
        Dict avec 'unlocked' et 'locked'
    """
    db = get_db()
    
    try:
        # Achievements débloqués
        unlocked_query = db.query(Achievement, UserAchievement).join(
            UserAchievement, Achievement.id == UserAchievement.achievement_id
        ).filter(UserAchievement.user_id == user_id).all()
        
        unlocked = [{
            'id': ach.id,
            'code': ach.code,
            'name': ach.name,
            'description': ach.description,
            'icon': ach.icon,
            'xp_reward': ach.xp_reward,
            'unlocked_at': ua.unlocked_at
        } for ach, ua in unlocked_query]
        
        # Tous les achievements
        all_achievements = db.query(Achievement).all()
        unlocked_ids = {ach['id'] for ach in unlocked}
        
        # Achievements verrouillés
        locked = [{
            'id': ach.id,
            'code': ach.code,
            'name': ach.name,
            'description': ach.description,
            'icon': ach.icon,
            'xp_reward': ach.xp_reward
        } for ach in all_achievements if ach.id not in unlocked_ids]
        
        return {
            'unlocked': unlocked,
            'locked': locked,
            'total': len(all_achievements),
            'unlocked_count': len(unlocked)
        }
        
    finally:
        db.close()


def get_level_info(xp_points: int) -> Dict:
    """
    Calcule les informations de niveau basées sur les XP
    
    Returns:
        Dict avec level, progress, xp_to_next_level, etc.
    """
    current_level = (xp_points // XP_PER_LEVEL) + 1
    current_level = min(current_level, MAX_LEVEL)  # Cap au max
    
    xp_current_level = (current_level - 1) * XP_PER_LEVEL
    xp_next_level = current_level * XP_PER_LEVEL
    xp_in_level = xp_points - xp_current_level
    progress_percent = (xp_in_level / XP_PER_LEVEL) * 100
    xp_to_next = xp_next_level - xp_points
    
    # Déterminer le titre
    if current_level >= 41:
        title = "Élite"
    elif current_level >= 26:
        title = "Avancé"
    elif current_level >= 11:
        title = "Intermédiaire"
    else:
        title = "Débutant"
    
    return {
        'current_level': current_level,
        'xp_total': xp_points,
        'xp_in_level': xp_in_level,
        'xp_to_next_level': xp_to_next if current_level < MAX_LEVEL else 0,
        'progress_percent': progress_percent,
        'title': title,
        'is_max_level': current_level >= MAX_LEVEL
    }


def calculate_daily_challenge() -> Dict:
    """
    Génère un challenge quotidien
    
    Returns:
        Dict avec type, description, goal, xp_reward
    """
    from datetime import date
    import random
    
    # Seed basée sur la date pour avoir le même challenge pour tous aujourd'hui
    today = date.today()
    random.seed(today.toordinal())
    
    challenges = [
        {
            'type': 'workouts',
            'description': 'Complétez 3 workouts aujourd\'hui',
            'goal': 3,
            'xp_reward': 100
        },
        {
            'type': 'perfect_score',
            'description': 'Obtenez un score >90% sur un workout',
            'goal': 90,
            'xp_reward': 80
        },
        {
            'type': 'total_time',
            'description': 'Entraînez-vous pendant 30 minutes',
            'goal': 1800,  # seconds
            'xp_reward': 75
        },
        {
            'type': 'all_exercises',
            'description': 'Faites au moins 3 types d\'exercices différents',
            'goal': 3,
            'xp_reward': 90
        }
    ]
    
    return random.choice(challenges)
