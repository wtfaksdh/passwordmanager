import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.exceptions import InvalidTag

# Импорт интерфейса EncryptionService (предполагается, что он определен в слое core)
from infrastructure import EncryptionService

class AESGCMService(EncryptionService):
    """
    Сервис шифрования AES-GCM (аутентифицированное шифрование) с помощью библиотеки cryptography.
    """
    def __init__(self, key: bytes):
        """
        :param key: секретный ключ AES (128/192/256 бит)
        """
        self._aesgcm = AESGCM(key)

    def encrypt(self, plaintext: bytes, associated_data: bytes = None) -> tuple[bytes, bytes]:
        """
        Шифрует данные AES-GCM.
        :param plaintext: данные для шифрования
        :param associated_data: дополнительные аутентифицируемые данные (можно None)
        :return: кортеж (nonce, ciphertext), где ciphertext содержит зашифрованные данные с тегом.
        """
        nonce = os.urandom(12)  # 96-bit nonce, рекомендуется NIST:contentReference[oaicite:10]{index=10}
        ciphertext = self._aesgcm.encrypt(nonce, plaintext, associated_data)
        return nonce, ciphertext

    def decrypt(self, nonce: bytes, ciphertext: bytes, associated_data: bytes = None) -> bytes:
        """
        Расшифровывает данные AES-GCM.
        :param nonce: nonce, использованный при шифровании
        :param ciphertext: зашифрованные данные (с включенным тегом)
        :param associated_data: доп. данные, переданные при шифровании (должны совпадать)
        :return: исходный plaintext
        :raises ValueError: если проверка аутентификационного тега не прошла.
        """
        try:
            return self._aesgcm.decrypt(nonce, ciphertext, associated_data)
        except InvalidTag as e:
            raise ValueError("Decryption failed: invalid tag or incorrect key/nonce") from e
