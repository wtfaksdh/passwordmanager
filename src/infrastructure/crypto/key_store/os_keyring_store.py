import base64
import keyring

# Импорт интерфейса KeyStoreService из слоя core
from core.ports.key_store import KeyStoreService

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

    def store_key(self, user_id: int, key: bytes) -> None:
        """
        Сохраняет ключ в keyring (в закодированном виде).
        :param user_id: идентификатор пользователя
        :param key: байтовый ключ для сохранения
        """
        encoded = base64.b64encode(key).decode('utf-8')
        keyring.set_password(self.service_name, str(user_id), encoded)

    def get_key(self, user_id: int) -> bytes:
        """
        Получает ключ из keyring.
        :param user_id: идентификатор пользователя
        :return: байтовый ключ, раскодированный из base64, или None если ключ не найден
        """
        encoded = keyring.get_password(self.service_name, str(user_id))
        if encoded is None:
            return None
        return base64.b64decode(encoded)
