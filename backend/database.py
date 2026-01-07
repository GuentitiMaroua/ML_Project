"""
Configuration de la base de données SQLAlchemy
"""
from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

# Chemin vers la BDD SQLite
BASE_DIR = Path(__file__).parent.parent
DB_PATH = BASE_DIR / "data" / "smartcoach.db"
DB_PATH.parent.mkdir(exist_ok=True)

DATABASE_URL = f"sqlite:///{DB_PATH}"

# Configuration du moteur avec pool de connexions
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # Required for SQLite
    echo=False,  # Set to True for SQL debugging
    pool_size=10,          # Connection pool size
    max_overflow=20,       # Extra connections beyond pool_size
    pool_pre_ping=True,    # Verify connections before using
    pool_recycle=3600      # Recycle connections after 1 hour
)

logger.info(f"Database engine configured: {DATABASE_URL}")

# Enable foreign keys for SQLite
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_conn, connection_record):
    cursor = dbapi_conn.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

# Session factory
SessionLocal = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)

# Base class for models
Base = declarative_base()


def get_db():
    """
    Dependency pour obtenir une session de base de données
    Usage: db = get_db()
    """
    db = SessionLocal()
    try:
        return db
    finally:
        pass  # Session will be closed manually


def init_db():
    """
    Initialise la base de données en créant toutes les tables
    """
    # Créer le dossier data s'il n'existe pas
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    # Import all models to register them
    from backend import models
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    print(f"✅ Base de données initialisée: {DB_PATH}")


def drop_all_tables():
    """
    Supprime toutes les tables (ATTENTION: utiliser seulement en développement)
    """
    Base.metadata.drop_all(bind=engine)
    print("⚠️ Toutes les tables ont été supprimées")


def reset_db():
    """
    Reset complet de la base de données
    """
    drop_all_tables()
    init_db()
    print("🔄 Base de données réinitialisée")


if __name__ == "__main__":
    # Test de la connexion
    print(f"Database URL: {DB_URL}")
    init_db()
