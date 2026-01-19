"""
Tests basiques pour SmartCoach Pro
Validation des fonctionnalités critiques
"""
import pytest
from backend.auth import validate_password, validate_email, hash_password, verify_password
from backend.models import User
from src.ml_predictor import get_ml_predictor
import pandas as pd
import numpy as np


class TestAuthentication:
    """Tests du système d'authentification"""
    
    def test_password_validation_strong(self):
        """Test validation mot de passe fort"""
        is_valid, msg = validate_password("SecurePass123!")
        assert is_valid == True
    
    def test_password_validation_weak(self):
        """Test rejet mot de passe faible"""
        is_valid, msg = validate_password("weak")
        assert is_valid == False
    
    def test_email_validation(self):
        """Test validation email"""
        assert validate_email("test@example.com") == True
        assert validate_email("invalid-email") == False
    
    def test_password_hashing(self):
        """Test hashage et vérification mot de passe"""
        password = "TestPassword123!"
        hashed = hash_password(password)
        
        # Hash différent du mot de passe
        assert hashed != password
        
        # Vérification fonctionne
        assert verify_password(password, hashed) == True
        assert verify_password("WrongPassword", hashed) == False


class TestMLPredictor:
    """Tests du système ML"""
    
    def test_ml_predictor_available(self):
        """Test disponibilité du modèle ML"""
        predictor = get_ml_predictor()
        assert predictor.is_available() == True
    
    def test_ml_prediction_returns_confidence(self):
        """Test que predict retourne confiance"""
        predictor = get_ml_predictor()
        
        if predictor.is_available():
            # Signal aléatoire pour test
            signal = pd.DataFrame({
                'time': np.linspace(0, 10, 500),
                'acc_x': np.random.randn(500),
                'acc_y': np.random.randn(500),
                'acc_z': np.random.randn(500),
                'gyr_x': np.random.randn(500),
                'gyr_y': np.random.randn(500),
                'gyr_z': np.random.randn(500)
            })
            
            exercise, confidence, probs = predictor.predict(signal)
            
            # Confiance entre 0 et 1
            assert 0 <= confidence <= 1
            assert isinstance(confidence, float)


class TestDatabase:
    """Tests du système database"""
    
    def test_database_url_from_env(self):
        """Test chargement DATABASE_URL depuis .env"""
        from backend.database import DB_URL
        assert DB_URL is not None
        assert "sqlite" in DB_URL or "postgresql" in DB_URL
    
    def test_database_tables_exist(self):
        """Test que toutes les tables existent"""
        from backend.database import engine
        from sqlalchemy import inspect
        
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        required_tables = [
            'users', 'workouts', 'programs', 
            'achievements', 'user_stats'
        ]
        
        for table in required_tables:
            assert table in tables, f"Table {table} manquante"


class TestPerformance:
    """Tests de performance"""
    
    def test_workout_table_has_indexes(self):
        """Test que la table workouts a des index"""
        from backend.database import engine
        from sqlalchemy import inspect
        
        inspector = inspect(engine)
        indexes = inspector.get_indexes('workouts')
        
        # Au moins 1 index (timestamp déjà présent)
        assert len(indexes) >= 1


# Configuration pytest
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
