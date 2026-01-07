# SmartCoach Pro - Application de Fitness Intelligente

## Description

**SmartCoach Pro** est une application complète de fitness utilisant l'Intelligence Artificielle pour analyser et améliorer vos performances sportives. L'application combine apprentissage automatique, visualisation de données et gamification pour offrir une expérience d'entraînement personnalisée et motivante.

---

## Fonctionnalités Principales

### 1. Système d'Authentification Sécurisé

**Page Login:**
- **Inscription** avec validation stricte des mots de passe
  - Minimum 8 caractères
  - Au moins 1 majuscule, 1 minuscule, 1 chiffre, 1 caractère spécial
  - Vérification des mots de passe communs
- **Connexion** avec protection contre les attaques
  - Rate limiting: 5 tentatives maximum par 15 minutes
  - Verrouillage automatique du compte après échec
  - Messages d'erreur sécurisés
- **Indicateur de force du mot de passe** en temps réel
- **Design ultra-moderne** avec glassmorphism et animations

**Sécurité Backend:**
- Hashage des mots de passe avec bcrypt
- Protection contre les attaques brute-force
- Logging de tous les événements d'authentification

---

### 2. Dashboard Personnel

**Vue d'ensemble des performances:**

**Métriques principales:**
- **Total XP**: Points d'expérience accumulés
- **Total Workouts**: Nombre d'entraînements effectués
- **Current Streak**: Jours consécutifs d'entraînement
- **Achievements Unlocked**: Succès débloqués

**Informations de niveau:**
- Niveau actuel de l'utilisateur
- Titre associé (Beginner, Intermediate, Advanced, etc.)
- Barre de progression vers le niveau suivant
- XP requis pour le prochain niveau

**Programme actif:**
- Nom du programme d'entraînement en cours
- Jour actuel / Nombre total de jours
- Pourcentage de progression
- Barre de progression visuelle

**Aperçu des achievements:**
- Top 3 des derniers succès débloqués
- Récompenses XP associées
- Lien vers la page complète

**Quick Actions:**
- Bouton "Start Workout" - Lancer un entraînement
- Bouton "Browse Programs" - Parcourir les programmes
- Bouton "View History" - Consulter l'historique

---

### 3. Page Workout - Entraînement IA

**Sélection d'exercice:**
- **Mode Manuel**: Choisir l'exercice dans une liste
  - Squat, Push-up, Curl, Plank, etc.
- **Mode Auto-Détection IA**: Le modèle ML détecte automatiquement l'exercice

**Paramètres avancés (repliables):**
- **Durée**: 5-20 secondes (réglable)
- **Fréquence d'échantillonnage**: 30-100 Hz (réglable)

**Processus d'entraînement:**
1. Cliquer sur "START WORKOUT"
2. Génération du signal d'accélération (3 axes X, Y, Z)
3. Analyse du mouvement en temps réel
4. Détection AI (si activée) avec niveau de confiance
5. Affichage des résultats

**Résultats affichés:**
- **Métriques de performance:**
  - Nombre de répétitions
  - Durée totale
  - Score de performance (%)
  - Régularité du mouvement (%)
  
- **Visualisation graphique:**
  - Graphique interactif 3 axes (Plotly)
  - Données d'accélération X, Y, Z
  - Zoom, hover, export possible

- **Feedback IA:**
  - Commentaire personnalisé du coach virtuel
  - Conseils d'amélioration
  - Encouragements

**Système d'achievements:**
- Vérification automatique après chaque workout
- Déblocage de nouveaux succès
- Animation de célébration (balloons)
- Récompenses XP instantanées

**Sauvegarde:**
- Enregistrement automatique dans la base de données
- Historique complet conservé
- Statistiques mises à jour

---

### 4. Page Programs - Programmes d'Entraînement

**Filtrage et tri:**
- **Filtrer par difficulté**: Beginner, Intermediate, Advanced, Expert
- **Trier par**: Nom, Difficulté, Durée

**Programmes disponibles:**
Chaque programme affiche:
- **Nom** du programme
- **Badge de difficulté** (couleur codée)
- **Description** détaillée
- **Durée** en semaines
- **Niveau** requis

**Programme actif:**
Si inscrit à un programme:
- Nom du programme en cours
- Progression jour/total
- Pourcentage d'avancement
- Barre de progression visuelle

**Inscription:**
- Bouton "Enroll in Program"
- Confirmation d'inscription
- Un seul programme actif à la fois
- Badge "Currently Enrolled" si actif

**Informations:**
- Description des niveaux (Beginner, Intermediate, Advanced, Expert)
- Guide de sélection du bon programme
- Conseils de progression

---

### 5. Page Achievements - Succès

**Progression globale:**
- **Barre de progression totale**
- **Nombre débloqués / Total**
- **Métriques:**
  - Unlocked: Nombre de succès obtenus
  - Locked: Nombre restant à débloquer

**Succès débloqués:**
- **Affichage en grille** (3 colonnes)
- Pour chaque achievement:
  - Icône emoji
  - Nom du succès
  - Description
  - Récompense XP (+X XP)
  - Carte avec gradient vert

**Succès verrouillés:**
- **Affichage en grille** (3 colonnes)
- Affichage grisé/transparent
- Icônes en grayscale
- Prérequis à compléter

**Conseils de déblocage:**
- Stay Consistent: Entraînements réguliers
- Try Different Exercises: Varier les exercices
- Aim for Quality: Viser les scores élevés
- Join Programs: Compléter les programmes
- Build Streaks: Maintenir les séries

---

### 6. Page History - Historique Détaillé

**Statistiques 30 jours:**
- **Total Workouts**: Nombre d'entraînements
- **Average Score**: Score moyen (%)
- **Best Score**: Meilleur score (%)
- **Favorite Exercise**: Exercice préféré

**Graphique d'évolution:**
- **Courbe de performance** (score par workout)
- **Ligne de tendance** (moyenne mobile sur 5 workouts)
- **Graphique interactif** Plotly
- Zoom, pan, hover pour détails
- Axes: Date vs Score (%)

**Distributions:**

**Exercise Distribution (Pie Chart):**
- Répartition par type d'exercice
- Pourcentages visuels
- Couleurs distinctes

**Score Distribution (Histogram):**
- Distribution des scores
- 10 bins
- Analyse de la performance globale

**Table détaillée:**
- **Colonnes:**
  - Date (YYYY-MM-DD HH:MM)
  - Exercise (nom)
  - Reps (répétitions)
  - Score (%)
  - Duration (secondes)
- **Pagination** / scrolling
- **Hauteur fixe** (400px)

**Export CSV:**
- Bouton "Export to CSV"
- Téléchargement instantané
- Nom du fichier avec date
- Toutes les données incluses

---

## Système de Gamification

### Niveaux et XP

**Système de progression:**
- 50 niveaux au total
- Formule XP: `level² × 100`
- Titres associés:
  - Niveaux 1-10: Beginner, Novice
  - Niveaux 11-20: Intermediate, Skilled
  - Niveaux 21-30: Advanced, Expert
  - Niveaux 31-40: Master, Elite
  - Niveaux 41-50: Champion, Legend

**Gains XP:**
- Compléter un workout: +50 XP (base)
- Score élevé: bonus XP
- Débloquer un achievement: +100 à +500 XP
- Compléter un programme: +1000 XP

### Achievements

**15 succès disponibles:**
1. **Premier Pas** - Premier workout (+100 XP)
2. **Semaine Parfaite** - 7 jours consécutifs (+300 XP)
3. **Étoile Montante** - 10 workouts (+200 XP)
4. **Gain Musculaire** - 10 séries de musculation (+300 XP)
5. **Perfectionniste** - Score >95% sur 10 workouts (+350 XP)
6. **Volonté de Fer** - 30 jours consécutifs (+400 XP)
7. **En Feu!** - 7 jours consécutifs (+250 XP)
8. **Le Centenaire** - 100 workouts (+500 XP)
9. **Marathonien** - 50 heures d'entraînement (+350 XP)
10. **Athlète Élite** - Niveau 25 (+500 XP)
11. **Démon de Vitesse** - 15 workouts en 2 semaines (+300 XP)
12. **Lève-tôt** - 10 workouts avant 8h (+200 XP)
13. **Oiseau de Nuit** - 10 workouts après 22h (+200 XP)
14. **Amateur de Variété** - Tous les types d'exercice (+300 XP)
15. **Légende** - Niveau 50 (+1000 XP)

---

## Intelligence Artificielle

### Classificateur d'Exercices

**Modèle ML:**
- **Algorithme**: Random Forest Classifier
- **Features**: Statistiques du signal (moyenne, variance, min, max, etc.)
- **Axes**: Accélération X, Y, Z
- **Fichier**: `models/exercise_classifier.pkl`

**Entraînement:**
- Données générées synthétiquement
- Patterns spécifiques par exercice
- Validation croisée
- Accuracy: ~95%

**Prédiction:**
- Input: Signaux d'accélération (3 axes)
- Output: Type d'exercice + Confiance (%)
- Temps réel pendant workout

### Analyse de Mouvement

**MovementAnalyzer:**
- Calcul du nombre de répétitions (détection de pics)
- Score de performance basé sur:
  - Amplitude des mouvements
  - Régularité
  - Vitesse d'exécution
- Régularité: Consistance entre répétitions
- Vitesse moyenne: Temps par répétition

### Coach IA

**Génération de feedback:**
- Analyse du score obtenu
- Conseils personnalisés
- Messages motivants
- Suggestions d'amélioration
- Basé sur:
  - Score de performance
  - Régularité
  - Nombre de répétitions
  - Vitesse

---

## Base de Données

### Schéma SQLite

**Table `users`:**
- `id` (Integer, Primary Key)
- `username` (String, Unique)
- `email` (String, Unique)
- `password_hash` (String)
- `created_at` (DateTime)
- `last_login` (DateTime)
- `is_active` (Boolean)

**Table `user_stats`:**
- `id` (Integer, Primary Key)
- `user_id` (Foreign Key → users)
- `xp_points` (Integer, default 0)
- `total_workouts` (Integer, default 0)
- `current_streak` (Integer, default 0)
- `longest_streak` (Integer, default 0)
- `total_training_time` (Integer, default 0)

**Table `workouts`:**
- `id` (Integer, Primary Key)
- `user_id` (Foreign Key → users)
- `exercise` (String)
- `repetitions` (Integer)
- `duration` (Integer)
- `score` (Float)
- `regularity` (Float)
- `speed` (Float)
- `feedback` (Text)
- `ai_detected` (Boolean)
- `confidence` (Float, nullable)
- `timestamp` (DateTime)

**Table `achievements`:**
- `id` (Integer, Primary Key)
- `name` (String)
- `description` (Text)
- `xp_reward` (Integer)
- `icon` (String)

**Table `user_achievements`:**
- `id` (Integer, Primary Key)
- `user_id` (Foreign Key → users)
- `achievement_id` (Foreign Key → achievements)
- `unlocked_at` (DateTime)

**Table `training_programs`:**
- `id` (Integer, Primary Key)
- `name` (String)
- `description` (Text)
- `difficulty` (String)
- `duration_weeks` (Integer)

**Table `user_programs`:**
- `id` (Integer, Primary Key)
- `user_id` (Foreign Key → users)
- `program_id` (Foreign Key → training_programs)
- `current_day` (Integer)
- `started_at` (DateTime)
- `is_active` (Boolean)

---

## Technologies Utilisées

### Frontend
- **Streamlit** (1.32.0) - Framework UI rapide
- **Plotly** (5.24.0) - Visualisations interactives
- **CSS3** - Styling moderne (glassmorphism, animations)

### Backend
- **Python** (3.13)
- **SQLAlchemy** (2.0.31) - ORM
- **SQLite** - Base de données
- **Bcrypt** (4.2.0) - Hashage sécurisé

### Machine Learning
- **Scikit-learn** (1.5.2) - Classificateur
- **NumPy** (2.1.1) - Calculs numériques
- **Pandas** (2.2.2) - Manipulation données

### Autres
- **SciPy** (1.14.1) - Signal processing
- **Logging** - Système de logs

---

## Structure du Projet

```
ML_Project/
│
├── app.py                          # Point d'entrée principal
├── requirements.txt                # Dépendances Python
├── styles.css                      # Styles CSS globaux
├── .gitignore                      # Fichiers ignorés par Git
│
├── backend/                        # Logique backend
│   ├── __init__.py
│   ├── auth.py                     # Authentification
│   ├── database.py                 # Configuration DB
│   ├── models.py                   # Modèles SQLAlchemy
│   ├── security.py                 # Rate limiting, validation
│   ├── logging_config.py           # Configuration logging
│   └── services/
│       ├── workout_service.py      # Logique workouts
│       └── ai_coach_service.py     # Feedback IA
│
├── pages/                          # Pages de l'application
│   ├── __init__.py
│   ├── dashboard.py                # Dashboard principal
│   ├── workout.py                  # Page entraînement
│   ├── programs.py                 # Programmes d'entraînement
│   ├── achievements.py             # Succès
│   └── history.py                  # Historique
│
├── src/                            # Code source partagé
│   ├── __init__.py
│   ├── components.py               # Composants UI réutilisables
│   ├── design_system.py            # Tokens de design (couleurs)
│   ├── gamification.py             # Système gamification
│   ├── exercise_classifier.py      # Classificateur ML
│   ├── signal_generator.py         # Génération signaux
│   ├── movement_analyzer.py        # Analyse mouvement
│   ├── workout_programs.py         # Logique programmes
│   ├── dashboard_helpers.py        # Helpers dashboard
│   ├── auth_components.py          # Composants auth UI
│   └── config.py                   # Configuration app
│
├── models/                         # Modèles ML
│   └── exercise_classifier.pkl     # Modèle entraîné
│
├── data/                           # Base de données
│   └── smartcoach.db               # SQLite DB
│
├── assets/                         # Images/Assets
│   ├── login_bg_premium.png
│   ├── dashboard_background_pro.png
│   ├── workout_background_pro.png
│   └── achievements_background_pro.png
│
└── logs/                           # Fichiers de logs
    └── app.log
```

---

## Installation

### Prérequis
- Python 3.13 ou supérieur
- pip (gestionnaire de packages Python)

### Étapes

1. **Cloner le projet:**
```bash
git clone <url-du-repo>
cd ML_Project
```

2. **Créer un environnement virtuel (recommandé):**
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

3. **Installer les dépendances:**
```bash
pip install -r requirements.txt
```

4. **Lancer l'application:**
```bash
streamlit run app.py
```

5. **Ouvrir dans le navigateur:**
```
http://localhost:8502
```

---

## Guide d'Utilisation

### Première Utilisation

1. **Créer un compte:**
   - Aller sur l'onglet "Create Account"
   - Entrer username, email, password
   - Mot de passe fort requis
   - Cliquer "Create Account"

2. **Se connecter:**
   - Onglet "Sign In"
   - Entrer credentials
   - Cliquer "Sign In"

### Effectuer un Entraînement

1. Aller sur page "Workout"
2. Choisir exercice OU activer AI Auto-Detection
3. (Optionnel) Ajuster paramètres dans "Advanced Settings"
4. Cliquer "START WORKOUT"
5. Attendre l'analyse
6. Consulter résultats et feedback
7. Répéter ou "Start Another Workout"

### Suivre un Programme

1. Aller sur "Programs"
2. Filtrer/trier programmes
3. Lire descriptions
4. Cliquer "Enroll in Program"
5. Suivre progression sur Dashboard

### Consulter l'Historique

1. Aller sur "History"
2. Voir statistiques 30 jours
3. Analyser graphiques de progression
4. Consulter table détaillée
5. (Optionnel) Exporter en CSV

---

## Équipe / Contributors

- **Votre équipe ici**

---

## License

Ce projet est développé dans le cadre d'un projet académique.

---



## Améliorations Futures

- [ ] Connexion avec Google/Facebook
- [ ] Mode dark/light
- [ ] Notifications push
- [ ] Application mobile
- [ ] Partage social
- [ ] Entraînement en groupe
- [ ] Vidéos de démonstration
- [ ] Reconnaissance vidéo en temps réel

---


