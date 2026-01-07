"""
Backend Security Module for SmartCoach Pro
Handles rate limiting, account lockout, and security utilities
"""
import time
from datetime import datetime, timedelta
from typing import Dict, Tuple, Optional
from collections import defaultdict
import hashlib


class RateLimiter:
    """Simple in-memory rate limiter for login attempts"""
    
    def __init__(self, max_attempts: int = 5, window_minutes: int = 15):
        self.max_attempts = max_attempts
        self.window_seconds = window_minutes * 60
        self.attempts: Dict[str, list] = defaultdict(list)
        self.locked_accounts: Dict[str, datetime] = {}
    
    def _clean_old_attempts(self, identifier: str):
        """Remove attempts older than the window"""
        cutoff = time.time() - self.window_seconds
        self.attempts[identifier] = [
            timestamp for timestamp in self.attempts[identifier]
            if timestamp > cutoff
        ]
    
    def is_locked(self, identifier: str) -> Tuple[bool, Optional[int]]:
        """
        Check if an account/IP is locked
        
        Returns:
            (is_locked, seconds_until_unlock)
        """
        if identifier in self.locked_accounts:
            unlock_time = self.locked_accounts[identifier]
            if datetime.utcnow() < unlock_time:
                remaining = (unlock_time - datetime.utcnow()).total_seconds()
                return True, int(remaining)
            else:
                # Unlock expired
                del self.locked_accounts[identifier]
                self.attempts[identifier] = []
        
        return False, None
    
    def record_attempt(self, identifier: str) -> Tuple[bool, int]:
        """
        Record a login attempt
        
        Returns:
            (is_allowed, remaining_attempts)
        """
        self._clean_old_attempts(identifier)
        
        # Check if already locked
        is_locked, _ = self.is_locked(identifier)
        if is_locked:
            return False, 0
        
        # Record this attempt
        self.attempts[identifier].append(time.time())
        attempts_count = len(self.attempts[identifier])
        
        # Lock if max attempts exceeded
        if attempts_count >= self.max_attempts:
            self.locked_accounts[identifier] = datetime.utcnow() + timedelta(minutes=15)
            return False, 0
        
        remaining = self.max_attempts - attempts_count
        return True, remaining
    
    def reset_attempts(self, identifier: str):
        """Reset attempts for successful login"""
        if identifier in self.attempts:
            del self.attempts[identifier]
        if identifier in self.locked_accounts:
            del self.locked_accounts[identifier]


# Global rate limiter instance
_rate_limiter = RateLimiter(max_attempts=5, window_minutes=15)


def get_rate_limiter() -> RateLimiter:
    """Get the global rate limiter instance"""
    return _rate_limiter


def hash_identifier(identifier: str) -> str:
    """Hash an identifier (username/IP) for privacy"""
    return hashlib.sha256(identifier.encode()).hexdigest()[:16]


def check_password_strength(password: str) -> Tuple[int, str]:
    """
    Check password strength
    
    Returns:
        (strength_score, description)
        strength_score: 0-4 (weak to very strong)
    """
    score = 0
    feedback = []
    
    # Length check
    if len(password) >= 8:
        score += 1
    if len(password) >= 12:
        score += 1
    else:
        feedback.append("Use 12+ characters")
    
    # Character variety
    has_lower = any(c.islower() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)
    
    variety_score = sum([has_lower, has_upper, has_digit, has_special])
    
    if variety_score >= 3:
        score += 1
    if variety_score == 4:
        score += 1
    
    if not has_upper:
        feedback.append("Add uppercase letters")
    if not has_digit:
        feedback.append("Add numbers")
    if not has_special:
        feedback.append("Add special characters")
    
    # Descriptions
    descriptions = {
        0: "Very Weak",
        1: "Weak",
        2: "Fair",
        3: "Strong",
        4: "Very Strong"
    }
    
    description = descriptions.get(score, "Weak")
    
    if feedback:
        description += f" - {', '.join(feedback)}"
    
    return score, description


# Common weak passwords to reject
WEAK_PASSWORDS = {
    "password", "123456", "12345678", "qwerty", "abc123",
    "password123", "admin", "letmein", "welcome", "monkey"
}


def is_common_password(password: str) -> bool:
    """Check if password is too common/weak"""
    return password.lower() in WEAK_PASSWORDS
