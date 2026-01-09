from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Any
import re

class CipherType(Enum):
    FERNET = "FERNET"
    AES_GCM = "AES_GCM"