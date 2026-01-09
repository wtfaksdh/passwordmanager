import secrets
import string

class PasswordMasker:
    @staticmethod
    def mask(password: str, visible: int = 2) -> str:
        if len(password) <= visible:
            return "*" * len(password)
        return "*" * (len(password) - visible) + password[-visible:]