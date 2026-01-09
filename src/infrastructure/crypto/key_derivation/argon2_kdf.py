from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from core.domain import EncryptedPassword, CipherType
from core.ports.encryption import EncryptionService
from core.ports.key_derivation import KeyDerivationService
from infrastructure import Type, Argon2

import os
import base64

class Argon2KeyDerivation(KeyDerivationService):
    def derive_key(self, password: str, salt: bytes) -> bytes:
        kdf = Argon2(
            time_cost=2,
            memory_cost=102400,
            parallelism=8,
            length=32,
            salt=salt,
            type=Type.ID
        )
        return kdf.derive(password.encode('utf-8'))