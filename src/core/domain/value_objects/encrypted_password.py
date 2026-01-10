from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Any
import re
from core.domain.enums.cipher_type import CipherType

@dataclass
class EncryptedPassword:
    ciphertext: bytes
    cipher_type: CipherType
    nonce: bytes | None = None  # Для AES-GCM: вектор инициализации
    tag: bytes | None = None    # Для AES-GCM: аутентификационный тег

    def serialize(self) -> bytes:
        """
        Сериализация шифрованного пароля для хранения.
        Для AES-GCM конкатенируем nonce + tag + ciphertext.
        """
        if self.cipher_type == CipherType.AES_GCM:
            if self.nonce is None or self.tag is None:
                raise ValueError("Nonce and tag must be set for AES-GCM.")
            return self.nonce + self.tag + self.ciphertext
        elif self.cipher_type == CipherType.FERNET:
            return self.ciphertext
        else:
            raise ValueError(f"Unsupported cipher type: {self.cipher_type}")

    @staticmethod
    def deserialize(data: bytes, cipher_type: CipherType) -> EncryptedPassword:
        """
        Десериализация из байтов в EncryptedPassword.
        Для AES-GCM извлекаем nonce (12), tag (16) и ciphertext.
        """
        if cipher_type == CipherType.AES_GCM:
            nonce = data[:12]
            tag = data[12:28]
            ciphertext = data[28:]
            return EncryptedPassword(ciphertext=ciphertext, cipher_type=cipher_type, nonce=nonce, tag=tag)
        elif cipher_type == CipherType.FERNET:
            return EncryptedPassword(ciphertext=data, cipher_type=CipherType.FERNET)
        else:
            raise ValueError(f"Unsupported cipher type: {cipher_type}")