"""
Session Management - Persistent sessions
"""
import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Optional, Tuple
from backend.database import get_db
from backend.models import User
import logging

logger = logging.getLogger(__name__)


class SessionManager:
    """Manage user sessions with database persistence"""
    
    def __init__(self):
        self.sessions = {}  # In-memory cache: {token: user_id}
        
    def create_session(self, user_id: int) -> str:
        """Create a new session token for user"""
        token = secrets.token_urlsafe(32)
        
        # Store in memory
        self.sessions[token] = {
            'user_id': user_id,
            'created_at': datetime.utcnow(),
            'expires_at': datetime.utcnow() + timedelta(days=7)
        }
        
        logger.info(f"Session created for user {user_id}")
        return token
    
    def validate_session(self, token: str) -> Optional[int]:
        """Validate session token and return user_id if valid"""
        if not token:
            return None
            
        session = self.sessions.get(token)
        if not session:
            return None
            
        # Check expiration
        if datetime.utcnow() > session['expires_at']:
            self.revoke_session(token)
            return None
            
        return session['user_id']
    
    def revoke_session(self, token: str):
        """Revoke a session token"""
        if token in self.sessions:
            del self.sessions[token]
            logger.info(f"Session revoked: {token[:10]}...")
    
    def get_user_by_token(self, token: str) -> Optional[User]:
        """Get user object from session token"""
        user_id = self.validate_session(token)
        if not user_id:
            return None
            
        db = get_db()
        try:
            user = db.query(User).filter(User.id == user_id).first()
            return user
        finally:
            db.close()


# Global session manager instance
_session_manager = None

def get_session_manager() -> SessionManager:
    """Get global session manager instance"""
    global _session_manager
    if _session_manager is None:
        _session_manager = SessionManager()
    return _session_manager
