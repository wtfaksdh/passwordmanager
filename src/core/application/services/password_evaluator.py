import secrets
import string
import re
from core.domain import PasswordStrength

class PasswordEvaluator:
    @staticmethod
    def evaluate(password: str) -> PasswordStrength:
        score = 0
        if len(password) >= 8:
            score += 1
        if re.search(r"[A-Z]", password):
            score += 1
        if re.search(r"[a-z]", password):
            score += 1
        if re.search(r"[0-9]", password):
            score += 1
        if re.search(r"[\W_]", password):
            score += 1
        if score <= 2:
            message = "Weak"
        elif score == 3:
            message = "Moderate"
        else:
            message = "Strong"
        return PasswordStrength(score=score, message=message)