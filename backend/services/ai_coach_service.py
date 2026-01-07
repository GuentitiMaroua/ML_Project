"""
Service de Coaching IA pour SmartCoach Pro
Génère des conseils personnalisés basés sur les performances
"""
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import random
from backend.database import get_db
from backend.models import Workout, UserStats


class AICoach:
    """Coach virtuel intelligent"""
    
    def __init__(self, use_openai: bool = False, api_key: Optional[str] = None):
        """
        Args:
            use_openai: Utiliser OpenAI GPT (nécessite clé API)
            api_key: Clé API OpenAI (optionnel)
        """
        self.use_openai = use_openai and api_key is not None
        self.api_key = api_key
        
        if self.use_openai:
            try:
                from openai import OpenAI
                self.client = OpenAI(api_key=api_key)
            except ImportError:
                print("⚠️ OpenAI non installé, utilisation du mode règles")
                self.use_openai = False
    
    def generate_workout_feedback(
        self,
        exercise: str,
        score: float,
        regularity: float,
        speed: float,
        repetitions: int
    ) -> str:
        """
        Génère un feedback détaillé sur un workout
        
        Returns:
            Message de feedback personnalisé
        """
        if self.use_openai:
            return self._generate_gpt_feedback(exercise, score, regularity, speed, repetitions)
        else:
            return self._generate_rule_based_feedback(exercise, score, regularity, speed, repetitions)
    
    def _generate_rule_based_feedback(
        self,
        exercise: str,
        score: float,
        regularity: float,
        speed: float,
        repetitions: int
    ) -> str:
        """Feedback basé sur des règles"""
        messages = []
        
        # Message principal basé sur le score
        if score >= 95:
            messages.append("🏆 Performance exceptionnelle! Vous êtes au top de votre forme!")
        elif score >= 90:
            messages.append("🔥 Excellent travail! Vous progressez magnifiquement!")
        elif score >= 75:
            messages.append("💪 Très bonne séance! Continuez sur cette lancée!")
        elif score >= 60:
            messages.append("👍 Bonne performance! Vous êtes sur la bonne voie.")
        else:
            messages.append("⚡ Performance moyenne. Ne vous découragez pas, chaque entraînement compte!")
        
        # Feedback sur la régularité
        if regularity >= 90:
            messages.append("Votre rythme est parfaitement régulier! Excellente technique.")
        elif regularity >= 75:
            messages.append("Bonne régularité dans l'exécution.")
        elif regularity < 60:
            messages.append("💡 Conseil: Concentrez-vous sur un rythme plus constant pour améliorer votre technique.")
        
        # Feedback sur la vitesse
        if speed > 100:
            messages.append("⚠️ Attention: Vous allez peut-être trop vite. Privilégiez la qualité à la quantité.")
        elif speed < 30:
            messages.append("💡 Conseil: Vous pouvez augmenter légèrement le rythme tout en gardant une bonne forme.")
        
        # Conseil spécifique à l'exercice
        exercise_tips = {
            'squat': "Pour des squats parfaits: gardez le dos droit et descendez jusqu'à ce que vos cuisses soient parallèles au sol.",
            'pushup': "Pompes efficaces: gardez le corps aligné et descendez jusqu'à ce que vos coudes forment un angle de 90°.",
            'curl': "Curls optimaux: Gard ez vos coudes fixes et concentrez-vous sur la contraction des biceps.",
            'jumping_jack': "Jumping jacks: Maintenez un rythme soutenu pour maximiser le cardio.",
            'plank': "Planche parfaite: Gardez le corps droit comme une planche, sans cambrer le dos."
        }
        
        if exercise in exercise_tips:
            messages.append(f"📝 {exercise_tips[exercise]}")
        
        return "\n".join(messages)
    
    def _generate_gpt_feedback(
        self,
        exercise: str,
        score: float,
        regularity: float,
        speed: float,
        repetitions: int
    ) -> str:
        """Feedback généré par GPT (si API disponible)"""
        try:
            prompt = f"""Tu es un coach sportif expert. Génère un feedback COURT (2-3 phrases) et encourageant en français sur cette performance:

Exercice: {exercise}
Score global: {score:.1f}%
Régularité: {regularity:.1f}%
Vitesse: {speed:.1f} reps/min
Répétitions: {repetitions}

Donne un feedback positif, spécifique et constructif. Utilise des emojis."""

            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=150,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"⚠️ Erreur GPT, fallback sur règles: {e}")
            return self._generate_rule_based_feedback(exercise, score, regularity, speed, repetitions)
    
    def analyze_progress(self, user_id: int, days: int = 30) -> Dict:
        """
        Analyse la progression d'un utilisateur
        
        Returns:
            Dict avec analyse et recommandations
        """
        db = get_db()
        
        try:
            start_date = datetime.utcnow() - timedelta(days=days)
            
            workouts = db.query(Workout).filter(
                Workout.user_id == user_id,
                Workout.timestamp >= start_date
            ).order_by(Workout.timestamp).all()
            
            if len(workouts) < 5:
                return {
                    'status': 'insufficient_data',
                    'message': "Continuez à vous entraîner pour obtenir une analyse détaillée de vos progrès!",
                    'recommendations': ["Effectuez au moins 5 workouts pour une analyse complète"]
                }
            
            # Calculer les tendances
            scores = [w.score for w in workouts]
            avg_score = sum(scores) / len(scores)
            
            # Tendance (première moitié vs deuxième moitié)
            mid = len( scores) // 2
            first_half_avg = sum(scores[:mid]) / len(scores[:mid])
            second_half_avg = sum(scores[mid:]) / len(scores[mid:])
            trend = second_half_avg - first_half_avg
            
            # Analyse
            if trend > 5:
                trend_message = "📈 Excellente progression! Vos performances s'améliorent constamment."
            elif trend > 0:
                trend_message = "📊 Légère progression. Vous êtes sur la bonne voie!"
            elif trend > -5:
                trend_message = "➡️ Performances stables. Peut-être temps d'augmenter l'intensité?"
            else:
                trend_message = "⚠️ Légère baisse de performance. Attention au surmenage, prenez du repos si nécessaire."
            
            # Recommandations
            recommendations = []
            
            if avg_score < 70:
                recommendations.append("Concentrez-vous sur la qualité plutôt que la quantité")
            
            # Vérifier la variété d'exercices
            exercises_done = set(w.exercise for w in workouts)
            if len(exercises_done) < 3:
                recommendations.append("Variez vos exercices pour un développement équilibré")
            
            # Fréquence
            workouts_per_week = len(workouts) / (days / 7)
            if workouts_per_week < 3:
                recommendations.append("Essayez d'augmenter la fréquence à 3-4 séances par semaine")
            elif workouts_per_week > 6:
                recommendations.append("Attention au surmenage: intégrez des jours de repos")
            
            return {
                'status': 'success',
                'avg_score': avg_score,
                'trend': trend,
                'trend_message': trend_message,
                'total_workouts': len(workouts),
                'workouts_per_week': workouts_per_week,
                'recommendations': recommendations if recommendations else ["Continue comme ça!"]
            }
            
        finally:
            db.close()
    
    def detect_plateau(self, user_id: int) -> Optional[str]:
        """
        Détecte si l'utilisateur est sur un plateau de performance
        
        Returns:
            Message d'alerte ou None
        """
        db = get_db()
        
        try:
            workouts = db.query(Workout).filter(
                Workout.user_id == user_id
            ).order_by(Workout.timestamp.desc()).limit(15).all()
            
            if len(workouts) < 15:
                return None
            
            scores = [w.score for w in reversed(workouts)]
            
            # Calculer variance
            mean = sum(scores) / len(scores)
            variance = sum((x - mean) ** 2 for x in scores) / len(scores)
            std_dev = variance ** 0.5
            
            # Si très faible variance et pas de progression
            if std_dev < 3 and mean < 85:
                return ("⚠️ Plateau détecté: Vos performances stagnent. "
                       "Essayez d'augmenter l'intensité ou de varier vos exercices!")
            
            return None
            
        finally:
            db.close()
    
    def get_daily_tip(self) -> str:
        """Retourne un conseil du jour aléatoire"""
        tips = [
            "💡 L'échauffement est essentiel: 5-10 minutes avant chaque séance!",
            "💪 La récupération fait partie de l'entraînement. Reposez-vous suffisamment!",
            "🥤 Hydratez-vous bien avant, pendant et après l'exercice.",
            "🎯 La régularité bat l'intensité: mieux vaut 3 séances moyennes qu'une seule intense.",
            "📈 Suivez vos progrès: cela booste la motivation!",
            "🧘 N'oubliez pas les étirements après l'entraînement.",
            "😴 Un bon sommeil (7-9h) est crucial pour la récupération musculaire.",
            "🍎 Une alimentation équilibrée potentialise vos entraînements.",
            "⏱️ La qualité du mouvement prime sur la quantité de répétitions.",
            "🎵 La musique peut augmenter vos performances de 15%!",
            "🏆 Célébrez chaque petite victoire, elles comptent toutes!",
            "📅 Planifiez vos séances à l'avance pour rester constant.",
            "💭 Visualisez vos objectifs pour rester motivé.",
            "🔄 Variez vos exercices toutes les 4-6 semaines pour éviter les plateaux.",
            "⚖️ Équilibrez cardio et renforcement musculaire."
        ]
        
        return random.choice(tips)


# Instance globale avec mode règles par défaut
coach = AICoach(use_openai=False)
