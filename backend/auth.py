"""
Système d'authentification pour SmartCoach Pro
Gestion login, register, sessions avec bcrypt
Sécurité renforcée avec rate limiting et validation avancée
"""
import bcrypt
from datetime import datetime
from typing import Optional, Tuple
import re
from backend.database import get_db
from backend.models import User, UserProfile, UserStats
from backend.security import (
    get_rate_limiter,
    hash_identifier,
    check_password_strength,
    is_common_password
)
from backend.logging_config import get_logger

logger = get_logger(__name__)


def hash_password(password: str) -> str:
    """
    Hash un mot de passe avec bcrypt
    
    Args:
        password: Mot de passe en clair
        
    Returns:
        Hash du mot de passe
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def verify_password(password: str, password_hash: str) -> bool:
    """
    Vérifie un mot de passe contre son hash
    
    Args:
        password: Mot de passe en clair
        password_hash: Hash stocké
        
    Returns:
        True si le mot de passe est correct
    """
    return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))


def validate_email(email: str) -> bool:
    """Valide le format d'un email"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_username(username: str) -> bool:
    """
    Valide un username
    - 3-50 caractères
    - Lettres, chiffres, underscore, tiret
    """
    if len(username) < 3 or len(username) > 50:
        return False
    pattern = r'^[a-zA-Z0-9_-]+$'
    return re.match(pattern, username) is not None


def validate_password(password: str) -> Tuple[bool, str]:
    """
    Valide un mot de passe avec critères renforcés
    - Minimum 8 caractères
    - Au moins une lettre majuscule et minuscule
    - Au moins un chiffre
    - Au moins un caractère spécial
    - Pas de mots de passe courants
    
    Returns:
        (is_valid, error_message)
    """
    # Check common passwords first
    if is_common_password(password):
        return False, "Ce mot de passe est trop commun. Choisissez-en un plus sécurisé."
    
    # Minimum length
    if len(password) < 8:
        return False, "Le mot de passe doit contenir au moins 8 caractères"
    
    # Character requirements
    if not any(c.islower() for c in password):
        return False, "Le mot de passe doit contenir au moins une lettre minuscule"
    
    if not any(c.isupper() for c in password):
        return False, "Le mot de passe doit contenir au moins une lettre majuscule"
    
    if not any(c.isdigit() for c in password):
        return False, "Le mot de passe doit contenir au moins un chiffre"
    
    if not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
        return False, "Le mot de passe doit contenir au moins un caractère spécial"
    
    return True, ""


def register_user(username: str, email: str, password: str) -> Tuple[bool, str, Optional[User]]:
    """
    Enregistre un nouvel utilisateur
    
    Args:
        username: Nom d'utilisateur
        email: Email
        password: Mot de passe
        
    Returns:
        (success, message, user)
    """
    db = get_db()
    
    try:
        # Validation username
        if not validate_username(username):
            return False, "Username invalide (3-50 caractères, lettres, chiffres, _, -)", None
        
        # Validation email
        if not validate_email(email):
            return False, "Email invalide", None
        
        # Validation password
        is_valid, error = validate_password(password)
        if not is_valid:
            return False, error, None
        
        # Vérifier si username existe déjà
        existing_user = db.query(User).filter(User.username == username).first()
        if existing_user:
            return False, "Ce nom d'utilisateur existe déjà", None
        
        # Vérifier si email existe déjà
        existing_email = db.query(User).filter(User.email == email).first()
        if existing_email:
            return False, "Cet email est déjà utilisé", None
        
        # Créer l'utilisateur
        password_hash = hash_password(password)
        new_user = User(
            username=username,
            email=email,
            password_hash=password_hash,
            created_at=datetime.utcnow(),
            is_premium=False,
            is_active=True
        )
        db.add(new_user)
        db.flush()  # Pour obtenir l'ID
        
        # Créer le profil
        profile = UserProfile(user_id=new_user.id)
        db.add(profile)
        
        # Créer les stats
        stats = UserStats(user_id=new_user.id)
        db.add(stats)
        
        db.commit()
        db.refresh(new_user)
        
        return True, "Compte créé avec succès!", new_user
        
    except Exception as e:
        db.rollback()
        return False, f"Erreur lors de la création du compte: {str(e)}", None
    finally:
        db.close()


def login_user(username_or_email: str, password: str) -> Tuple[bool, str, Optional[User]]:
    """
    Authentifie un utilisateur avec rate limiting et sécurité renforcée
    
    Args:
        username_or_email: Username ou email
        password: Mot de passe
        
    Returns:
        (success, message, user)
    """
    # Rate limiting check
    rate_limiter = get_rate_limiter()
    identifier = hash_identifier(username_or_email.lower())
    
    # Check if locked
    is_locked, seconds_remaining = rate_limiter.is_locked(identifier)
    if is_locked:
        minutes = seconds_remaining // 60
        return False, f"Compte temporairement verrouillé. Réessayez dans {minutes} minutes.", None
    
    # Record attempt
    is_allowed, remaining_attempts = rate_limiter.record_attempt(identifier)
    if not is_allowed:
        logger.warning(f"Too many login attempts for: {username_or_email}")
        return False, "Trop de tentatives. Compte verrouillé pour 15 minutes.", None
    
    db = get_db()
    
    try:
        # Chercher par username ou email
        user = db.query(User).filter(
            (User.username == username_or_email) | (User.email == username_or_email)
        ).first()
        
        if not user:
            logger.info(f"Login failed - user not found: {username_or_email}")
            if remaining_attempts > 0:
                return False, f"Identifiants incorrects. {remaining_attempts} tentatives restantes.", None
            return False, "Identifiants incorrects", None
        
        if not user.is_active:
            logger.info(f"Login failed - account disabled: {user.username}")
            return False, "Compte désactivé. Contactez le support.", None
        
        # Vérifier le mot de passe
        if not verify_password(password, user.password_hash):
            logger.info(f"Login failed - wrong password: {user.username}")
            if remaining_attempts > 0:
                return False, f"Identifiants incorrects. {remaining_attempts} tentatives restantes.", None
            return False, "Identifiants incorrects", None
        
        # Success - reset attempts
        rate_limiter.reset_attempts(identifier)
        
        # Mettre à jour last_login
        user.last_login = datetime.utcnow()
        db.commit()
        db.refresh(user)
        
        logger.info(f"Login successful: {user.username}")
        return True, "Connexion réussie!", user
        
    except Exception as e:
        logger.error(f"Login error for {username_or_email}: {str(e)}")
        return False, f"Erreur lors de la connexion: {str(e)}", None
    finally:
        db.close()


def get_user_by_id(user_id: int) -> Optional[User]:
    """Récupère un utilisateur par son ID"""
    db = get_db()
    try:
        return db.query(User).filter(User.id == user_id).first()
    finally:
        db.close()


def get_user_by_username(username: str) -> Optional[User]:
    """Récupère un utilisateur par son username"""
    db = get_db()
    try:
        return db.query(User).filter(User.username == username).first()
    finally:
        db.close()


def update_password(user_id: int, old_password: str, new_password: str) -> Tuple[bool, str]:
    """
    Change le mot de passe d'un utilisateur
    
    Returns:
        (success, message)
    """
    db = get_db()
    
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return False, "Utilisateur non trouvé"
        
        # Vérifier l'ancien mot de passe
        if not verify_password(old_password, user.password_hash):
            return False, "Ancien mot de passe incorrect"
        
        # Valider le nouveau mot de passe
        is_valid, error = validate_password(new_password)
        if not is_valid:
            return False, error
        
        # Mettre à jour
        user.password_hash = hash_password(new_password)
        db.commit()
        
        return True, "Mot de passe modifié avec succès"
        
    except Exception as e:
        db.rollback()
        return False, f"Erreur: {str(e)}"
    finally:
        db.close()


def delete_user(user_id: int) -> Tuple[bool, str]:
    """
    Supprime un utilisateur (soft delete: is_active=False)
    
    Returns:
        (success, message)
    """
    db = get_db()
    
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return False, "Utilisateur non trouvé"
        
        user.is_active = False
        db.commit()
        
        return True, "Compte désactivé"
        
    except Exception as e:
        db.rollback()
        return False, f"Erreur: {str(e)}"
    finally:
        db.close()
