import sqlite3 
from datetime import datetime

class PasswordEntry:

    def __init__(self, entry_id=None, service="", username="", password=""):
        self.id = entry_id
        self.service = service
        self.username = username
        self.password = password

    #Строковое представление
    def __str__(self):
        return f"PasswordEntry(id={self.id}, service='{self.service}')"
    
    #Информация о записи
    def display(self, show_password=False):
        print(f"Сервис: {self.service}")
        print(f"Логин: {self.username}")
        if show_password:
            print(f"Пароль: {self.password}")
        else: 
            print(f"Пароль: {'*' * len(self.password)}")

    #Преобразование в словарь
    def to_dict(self):
        return {
            'id' : self.id,
            'service' : self.service,
            'username' : self.username,
            'password' : self.password
        }
    
    @classmethod
    #Объект из словоря
    def from_dict(cls, data):
        return cls(
            entry_id=data.get('id'),
            service=data.get('service', ''),
            username=data.get('username', ''),
            password=data.get('password', '')
        )