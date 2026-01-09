import secrets
import string

class PasswordGenerator:
    @staticmethod
    def generate(length: int = 12) -> str:
        alphabet = string.ascii_letters + string.digits + string.punctuation
        return ''.join(secrets.choice(alphabet) for _ in range(length))
