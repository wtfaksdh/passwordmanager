from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from core.domain import EncryptedPassword, CipherType
from core.ports.encryption import EncryptionService
import os
import base64


class EncryptionServiceImpl(EncryptionService):
    def encrypt(self, plaintext: str, key: bytes, cipher_type: CipherType) -> EncryptedPassword:
        data = plaintext.encode('utf-8')
        if cipher_type == CipherType.FERNET:
            # Преобразуем ключ в формат base64 для Fernet
            bkey = key
            if isinstance(key, bytes):
                bkey = base64.urlsafe_b64encode(key)
            fernet = Fernet(bkey)
            token = fernet.encrypt(data)
            return EncryptedPassword(ciphertext=token, cipher_type=CipherType.FERNET)
        elif cipher_type == CipherType.AES_GCM:
            nonce = os.urandom(12)
            encryptor = Cipher(
                algorithms.AES(key),
                modes.GCM(nonce),
                backend=default_backend()
            ).encryptor()
            ciphertext = encryptor.update(data) + encryptor.finalize()
            tag = encryptor.tag
            return EncryptedPassword(ciphertext=ciphertext, cipher_type=CipherType.AES_GCM, nonce=nonce, tag=tag)
        else:
            raise ValueError(f"Unsupported cipher: {cipher_type}")

    def decrypt(self, encrypted: EncryptedPassword, key: bytes) -> str:
        if encrypted.cipher_type == CipherType.FERNET:
            # Преобразуем ключ в формат base64 для Fernet
            bkey = key
            if isinstance(key, bytes):
                bkey = base64.urlsafe_b64encode(key)
            fernet = Fernet(bkey)
            plaintext = fernet.decrypt(encrypted.ciphertext)
            return plaintext.decode('utf-8')
        elif encrypted.cipher_type == CipherType.AES_GCM:
            if encrypted.nonce is None or encrypted.tag is None:
                raise ValueError("Missing nonce or tag for AES-GCM decryption.")
            decryptor = Cipher(
                algorithms.AES(key),
                modes.GCM(encrypted.nonce, encrypted.tag),
                backend=default_backend()
            ).decryptor()
            plaintext = decryptor.update(encrypted.ciphertext) + decryptor.finalize()
            return plaintext.decode('utf-8')
        else:
            raise ValueError(f"Unsupported cipher: {encrypted.cipher_type}")