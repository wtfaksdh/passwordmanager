#!/usr/bin/env python3
"""Initialize password manager database"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from src.database.db import init_db
from src.config import DB_PATH


def main():
    """Initialize database"""
    print(f"Initializing database at {DB_PATH}...")
    try:
        init_db()
        print("✅ Database initialized successfully!")
        print(f"📁 Database location: {DB_PATH}")
        return 0
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
