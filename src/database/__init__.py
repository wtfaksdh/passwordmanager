"""Database module for Password Manager"""
from .db import Database, init_db
from .models import User, Password

__all__ = ["Database", "init_db", "User", "Password"]
