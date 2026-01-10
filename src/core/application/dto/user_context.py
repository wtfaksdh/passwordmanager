from __future__ import annotations
from dataclasses import dataclass
from typing import List
import re

@dataclass
class UserContext:
    user_id: int