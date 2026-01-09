import base64
import keyring

# Импорт интерфейса KeyStoreService из слоя core
from core import KeyStoreService

class OSKeyringStore(KeyStoreService):
    """
    Хранилище ключей на основе системного keyring (keystore). 
    Ключ хранится в виде base64-строки.
    """
    def __init__(self, service_name: str):
        """
        :param service_name: имя сервиса (namespace) в keyring
        """
        self.service_name = service_name

    def set_key(self, key_name: str, key: bytes) -> None:
        """
        Сохраняет ключ в keyring (в закодированном виде).
        :param key_name: идентификатор ключа
        :param key: байтовый ключ для сохранения
        """
        encoded = base64.b64encode(key).decode('utf-8')
        keyring.set_password(self.service_name, key_name, encoded)
        # Пример использования keyring: keyring.set_password("sys", "user", "password"):contentReference[oaicite:13]{index=13}

    def get_key(self, key_name: str) -> bytes:
        """
        Получает ключ из keyring.
        :param key_name: идентификатор ключа
        :return: байтовый ключ, раскодированный из base64
        :raises KeyError: если ключ не найден
        """
        encoded = keyring.get_password(self.service_name, key_name)
        if encoded is None:
            raise KeyError(f"Key '{key_name}' not found in keyring")
        return base64.b64decode(encoded)