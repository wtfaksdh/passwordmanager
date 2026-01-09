from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from core.domain import EncryptedPassword, CipherType
from core.ports.encryption import EncryptionService
from core.ports.key_store import KeyStoreService
import os
import base64


class InMemoryKeyStore(KeyStoreService):
    def __init__(self):
        self._store: dict[int, bytes] = {}

    def store_key(self, user_id: int, key: bytes) -> None:
        self._store[user_id] = key

    def get_key(self, user_id: int) -> bytes:
        return self._store.get(user_id)