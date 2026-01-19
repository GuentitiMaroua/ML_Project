"""
Modèles SQLAlchemy pour SmartCoach Pro
Tous les modèles de données de l'application
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text, ForeignKey, JSON, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from backend.database import Base


# Enums
class FitnessLevel(enum.Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    ELITE = "elite"


class ProgramStatus(enum.Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    PAUSED = "paused"
    ABANDONED = "abandoned"


class GoalType(enum.Enum):
    WORKOUTS_PER_WEEK = "workouts_per_week"
    AVERAGE_SCORE = "average_score"
    WEIGHT_LOSS = "weight_loss"
    STRENGTH_GAIN = "strength_gain"
    COMPLETE_PROGRAM = "complete_program"


class GoalStatus(enum.Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class NotificationType(enum.Enum):
    ACHIEVEMENT = "achievement"
    REMINDER = "reminder"
    MILESTONE = "milestone"
    COACH_TIP = "coach_tip"
    STREAK_WARNING = "streak_warning"


# Models
class User(Base):
    """Modèle utilisateur"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime)
    is_premium = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    avatar_url = Column(String(255))
    
    # Relationships
    profile = relationship("UserProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    workouts = relationship("Workout", back_populates="user", cascade="all, delete-orphan")
    user_programs = relationship("UserProgram", back_populates="user", cascade="all, delete-orphan")
    achievements = relationship("UserAchievement", back_populates="user", cascade="all, delete-orphan")
    stats = relationship("UserStats", back_populates="user", uselist=False, cascade="all, delete-orphan")
    goals = relationship("Goal", back_populates="user", cascade="all, delete-orphan")
    notifications = relationship("Notification", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}')>"


class UserProfile(Base):
    """Profil détaillé utilisateur"""
    __tablename__ = "user_profiles"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    age = Column(Integer)
    weight = Column(Float)  # kg
    height = Column(Float)  # cm
    fitness_level = Column(Enum(FitnessLevel), default=FitnessLevel.BEGINNER)
    goals_description = Column(Text)
    preferences = Column(JSON)  # Diet, training days, etc.
    bio = Column(Text)
    
    # Relationship
    user = relationship("User", back_populates="profile")
    
    def __repr__(self):
        return f"<UserProfile(user_id={self.user_id}, level={self.fitness_level})>"


class Workout(Base):
    """Session d'entraînement"""
    __tablename__ = "workouts"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    exercise = Column(String(50), nullable=False, index=True)  # ✅ Index pour filtrage rapide
    repetitions = Column(Integer, nullable=False)
    duration = Column(Float, nullable=False)  # seconds
    score = Column(Float, nullable=False)
    regularity = Column(Float)
    speed = Column(Float)
    feedback = Column(Text)
    notes = Column(Text)
    detected_by_ai = Column(Boolean, default=False)
    ai_confidence = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Relationship
    user = relationship("User", back_populates="workouts")
    
    def __repr__(self):
        return f"<Workout(id={self.id}, exercise='{self.exercise}', score={self.score})>"


class Program(Base):
    """Programme d'entraînement"""
    __tablename__ = "programs"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    difficulty = Column(Enum(FitnessLevel), nullable=False)
    duration_weeks = Column(Integer, nullable=False)
    created_by = Column(String(50), default="system")  # system or user_id
    is_public = Column(Boolean, default=True)
    icon = Column(String(10))
    
    # Relationships
    exercises = relationship("ProgramExercise", back_populates="program", cascade="all, delete-orphan")
    user_programs = relationship("UserProgram", back_populates="program")
    
    def __repr__(self):
        return f"<Program(id={self.id}, name='{self.name}')>"


class ProgramExercise(Base):
    """Exercice dans un programme"""
    __tablename__ = "program_exercises"
    
    id = Column(Integer, primary_key=True)
    program_id = Column(Integer, ForeignKey("programs.id"), nullable=False)
    day = Column(Integer, nullable=False)  # Day 1, 2, 3, etc.
    exercise = Column(String(50), nullable=False)
    sets = Column(Integer, nullable=False)
    reps = Column(Integer, nullable=False)
    rest_time = Column(Integer)  # seconds
    order = Column(Integer)  # Order in the day
    notes = Column(Text)
    
    # Relationship
    program = relationship("Program", back_populates="exercises")
    
    def __repr__(self):
        return f"<ProgramExercise(program_id={self.program_id}, day={self.day}, exercise='{self.exercise}')>"


class UserProgram(Base):
    """Association utilisateur-programme avec progression"""
    __tablename__ = "user_programs"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    program_id = Column(Integer, ForeignKey("programs.id"), nullable=False)
    start_date = Column(DateTime, default=datetime.utcnow)
    current_day = Column(Integer, default=1)
    status = Column(Enum(ProgramStatus), default=ProgramStatus.ACTIVE)
    completion_date = Column(DateTime)
    
    # Relationships
    user = relationship("User", back_populates="user_programs")
    program = relationship("Program", back_populates="user_programs")
    
    def __repr__(self):
        return f"<UserProgram(user_id={self.user_id}, program_id={self.program_id}, status={self.status})>"


class Achievement(Base):
    """Définition des achievements/badges"""
    __tablename__ = "achievements"
    
    id = Column(Integer, primary_key=True)
    code = Column(String(50), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    icon = Column(String(10))
    xp_reward = Column(Integer, default=0)
    
    # Relationship
    user_achievements = relationship("UserAchievement", back_populates="achievement")
    
    def __repr__(self):
        return f"<Achievement(code='{self.code}', name='{self.name}')>"


class UserAchievement(Base):
    """Achievements débloqués par l'utilisateur"""
    __tablename__ = "user_achievements"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    achievement_id = Column(Integer, ForeignKey("achievements.id"), nullable=False)
    unlocked_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="achievements")
    achievement = relationship("Achievement", back_populates="user_achievements")
    
    def __repr__(self):
        return f"<UserAchievement(user_id={self.user_id}, achievement_id={self.achievement_id})>"


class UserStats(Base):
    """Statistiques globales utilisateur"""
    __tablename__ = "user_stats"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    total_workouts = Column(Integer, default=0)
    total_time = Column(Float, default=0.0)  # seconds
    xp_points = Column(Integer, default=0)
    level = Column(Integer, default=1, index=True)  # ✅ Index pour leaderboards
    current_streak = Column(Integer, default=0)
    best_streak = Column(Integer, default=0)
    last_workout_date = Column(DateTime)
    
    # Relationship
    user = relationship("User", back_populates="stats")
    
    def __repr__(self):
        return f"<UserStats(user_id={self.user_id}, level={self.level}, xp={self.xp_points})>"


class Goal(Base):
    """Objectif personnel utilisateur"""
    __tablename__ = "goals"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    type = Column(Enum(GoalType), nullable=False)
    target = Column(Float, nullable=False)
    current_progress = Column(Float, default=0.0)
    deadline = Column(DateTime)
    status = Column(Enum(GoalStatus), default=GoalStatus.ACTIVE)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)
    
    # Relationship
    user = relationship("User", back_populates="goals")
    
    def __repr__(self):
        return f"<Goal(user_id={self.user_id}, type={self.type}, progress={self.current_progress}/{self.target})>"


class Notification(Base):
    """Notifications in-app"""
    __tablename__ = "notifications"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    type = Column(Enum(NotificationType), nullable=False)
    message = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Relationship
    user = relationship("User", back_populates="notifications")
    
    def __repr__(self):
        return f"<Notification(user_id={self.user_id}, type={self.type}, read={self.is_read})>"
