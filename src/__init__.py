# -*- coding: utf-8 -*-
"""
SmartCoach Pro - Module Package
"""

from .signal_generator import SignalGenerator
from .movement_analyzer import MovementAnalyzer
from .exercise_classifier import ExerciseClassifier
from .config import (
    ICONS,
    EXERCISES,
    PERFORMANCE_LEVELS,
    CHALLENGES,
    USER_GOALS,
    MOTIVATIONAL_QUOTES,
    DEFAULT_SETTINGS,
    THEME_COLORS
)

__all__ = [
    'SignalGenerator',
    'MovementAnalyzer',
    'ExerciseClassifier',
    'ICONS',
    'EXERCISES',
    'PERFORMANCE_LEVELS',
    'CHALLENGES',
    'USER_GOALS',
    'MOTIVATIONAL_QUOTES',
    'DEFAULT_SETTINGS',
    'THEME_COLORS'
]

__version__ = '3.0.0'
__author__ = 'SmartCoach Pro Team'
