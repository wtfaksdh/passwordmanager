from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Any
import re

class UnauthorizedError(Exception):
    """Доступ к ресурсу не разрешён."""
    pass