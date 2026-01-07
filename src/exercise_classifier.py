"""
Module de classification automatique des exercices de musculation
Utilise un modèle de Machine Learning pour identifier le type d'exercice
"""
import numpy as np
from scipy import signal
from scipy.stats import skew, kurtosis
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import joblib
import os
from typing import Tuple, Optional, Dict
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ExerciseClassifier:
    """
    Classificateur intelligent pour la reconnaissance automatique d'exercices
    Utilise Random Forest avec features extraites des signaux d'accéléromètre
    """
    
    def __init__(self):
        """Initialise le classificateur"""
        self.model: Optional[RandomForestClassifier] = None
        self.scaler: Optional[StandardScaler] = None
        self.exercise_names = ['squat', 'pushup', 'curl', 'jumping_jack', 'plank']
        self.is_trained = False
        
    def extract_features(self, acc_x: np.ndarray, acc_y: np.ndarray, 
                        acc_z: np.ndarray) -> np.ndarray:
        """
        Extrait les features des signaux d'accéléromètre
        
        Features extraites (30 au total):
        - Statistiques par axe (mean, std, min, max, skew, kurtosis) = 18 features
        - Magnitude globale (mean, std, max) = 3 features
        - Fréquence dominante par axe (FFT) = 3 features
        - Énergie du signal par axe = 3 features
        - Corrélations entre axes = 3 features
        
        Args:
            acc_x: Accélération axe X
            acc_y: Accélération axe Y
            acc_z: Accélération axe Z
            
        Returns:
            Array de 30 features
        """
        features = []
        
        # 1. Statistiques pour chaque axe (6 features × 3 axes = 18)
        for axis in [acc_x, acc_y, acc_z]:
            features.extend([
                np.mean(axis),           # Moyenne
                np.std(axis),            # Écart-type
                np.min(axis),            # Minimum
                np.max(axis),            # Maximum
                skew(axis),              # Asymétrie
                kurtosis(axis)           # Aplatissement
            ])
        
        # 2. Magnitude vectorielle (3 features)
        magnitude = np.sqrt(acc_x**2 + acc_y**2 + acc_z**2)
        features.extend([
            np.mean(magnitude),
            np.std(magnitude),
            np.max(magnitude)
        ])
        
        # 3. Fréquence dominante par FFT (3 features)
        for axis in [acc_x, acc_y, acc_z]:
            fft_vals = np.abs(np.fft.fft(axis))
            fft_freq = np.fft.fftfreq(len(axis))
            # Ignorer la composante DC (fréquence 0)
            dominant_freq_idx = np.argmax(fft_vals[1:len(fft_vals)//2]) + 1
            dominant_freq = np.abs(fft_freq[dominant_freq_idx])
            features.append(dominant_freq)
        
        # 4. Énergie du signal (3 features)
        for axis in [acc_x, acc_y, acc_z]:
            energy = np.sum(axis**2) / len(axis)
            features.append(energy)
        
        # 5. Corrélations entre axes (3 features)
        features.extend([
            np.corrcoef(acc_x, acc_y)[0, 1],  # Corr X-Y
            np.corrcoef(acc_x, acc_z)[0, 1],  # Corr X-Z
            np.corrcoef(acc_y, acc_z)[0, 1]   # Corr Y-Z
        ])
        
        return np.array(features)
    
    def train(self, X: np.ndarray, y: np.ndarray, 
             n_estimators: int = 100) -> Dict[str, float]:
        """
        Entraîne le modèle de classification
        
        Args:
            X: Features (n_samples, n_features)
            y: Labels (n_samples,)
            n_estimators: Nombre d'arbres dans la forêt
            
        Returns:
            Dict avec métriques d'entraînement
        """
        logger.info(f"Début de l'entraînement avec {len(X)} échantillons")
        
        # Normalisation des features
        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(X)
        
        # Entraînement du Random Forest
        self.model = RandomForestClassifier(
            n_estimators=n_estimators,
            max_depth=15,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42,
            n_jobs=-1  # Utiliser tous les CPU
        )
        
        self.model.fit(X_scaled, y)
        self.is_trained = True
        
        # Calculer le score d'entraînement
        train_score = self.model.score(X_scaled, y)
        
        logger.info(f"Entraînement terminé. Score: {train_score:.2%}")
        
        return {
            'train_score': train_score,
            'n_samples': len(X),
            'n_features': X.shape[1]
        }
    
    def predict(self, acc_x: np.ndarray, acc_y: np.ndarray, 
               acc_z: np.ndarray) -> Tuple[str, float, np.ndarray]:
        """
        Prédit le type d'exercice à partir des signaux
        
        Args:
            acc_x, acc_y, acc_z: Signaux d'accéléromètre
            
        Returns:
            Tuple (exercice prédit, confiance, probabilités pour chaque classe)
        """
        if not self.is_trained or self.model is None or self.scaler is None:
            raise ValueError("Le modèle n'est pas entraîné. Appelez train() d'abord.")
        
        # Extraction des features
        features = self.extract_features(acc_x, acc_y, acc_z)
        features_scaled = self.scaler.transform(features.reshape(1, -1))
        
        # Prédiction
        prediction = self.model.predict(features_scaled)[0]
        probabilities = self.model.predict_proba(features_scaled)[0]
        
        # Confiance = probabilité max
        confidence = np.max(probabilities)
        
        # Mapping index -> nom d'exercice
        exercise = self.exercise_names[prediction]
        
        logger.info(f"Prédiction: {exercise} (confiance: {confidence:.2%})")
        
        return exercise, confidence, probabilities
    
    def get_feature_importance(self) -> Optional[np.ndarray]:
        """
        Retourne l'importance de chaque feature
        
        Returns:
            Array d'importance des features ou None si pas entraîné
        """
        if self.model is None:
            return None
        return self.model.feature_importances_
    
    def save_model(self, path: str = 'models/exercise_classifier.pkl') -> None:
        """
        Sauvegarde le modèle entraîné
        
        Args:
            path: Chemin de sauvegarde
        """
        if not self.is_trained:
            raise ValueError("Impossible de sauvegarder un modèle non entraîné")
        
        # Créer le dossier si nécessaire
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        # Sauvegarder le modèle et le scaler
        model_data = {
            'model': self.model,
            'scaler': self.scaler,
            'exercise_names': self.exercise_names,
            'is_trained': self.is_trained
        }
        
        joblib.dump(model_data, path)
        logger.info(f"Modèle sauvegardé dans {path}")
    
    def load_model(self, path: str = 'models/exercise_classifier.pkl') -> None:
        """
        Charge un modèle entraîné
        
        Args:
            path: Chemin du modèle
        """
        if not os.path.exists(path):
            raise FileNotFoundError(f"Modèle non trouvé: {path}")
        
        model_data = joblib.load(path)
        
        self.model = model_data['model']
        self.scaler = model_data['scaler']
        self.exercise_names = model_data['exercise_names']
        self.is_trained = model_data['is_trained']
        
        logger.info(f"Modèle chargé depuis {path}")
    
    def cross_validate(self, X: np.ndarray, y: np.ndarray, 
                      cv: int = 5) -> Dict[str, float]:
        """
        Validation croisée du modèle
        
        Args:
            X: Features
            y: Labels
            cv: Nombre de folds
            
        Returns:
            Dict avec scores de validation
        """
        from sklearn.model_selection import cross_val_score
        
        # Normalisation
        X_scaled = self.scaler.fit_transform(X) if self.scaler else StandardScaler().fit_transform(X)
        
        # Initialisation du modèle
        temp_model = RandomForestClassifier(
            n_estimators=100,
            max_depth=15,
            random_state=42
        )
        
        # Validation croisée
        scores = cross_val_score(temp_model, X_scaled, y, cv=cv)
        
        logger.info(f"Validation croisée ({cv}-fold): {scores.mean():.2%} (+/- {scores.std() * 2:.2%})")
        
        return {
            'mean_score': scores.mean(),
            'std_score': scores.std(),
            'scores': scores
        }
