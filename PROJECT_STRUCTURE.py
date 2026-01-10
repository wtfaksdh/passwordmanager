#!/usr/bin/env python3
"""
Project Structure Information
Generated: January 11, 2026
"""

PROJECT_STRUCTURE = {
    "root_files": {
        "main.py": "Application entry point",
        "config.py": "Configuration and settings",
        "requirements.txt": "Python dependencies",
        ".env": "Environment variables (create from .env.example)",
        ".env.example": "Environment template",
        ".gitignore": "Git ignore rules",
        "README.md": "Quick start guide",
        "STATUS.md": "Project status and features",
    },
    
    "src": {
        "bot": {
            "handlers": {
                "auth.py": "Authentication handlers (register, login, logout)",
                "password.py": "Password management handlers (CRUD operations)",
            },
            "states.py": "FSM states for user interactions",
            "keyboards.py": "Telegram keyboard layouts",
            "__init__.py": "Package initialization",
        },
        "database": {
            "db.py": "Database connection and initialization",
            "models.py": "Data models (User, Password)",
            "crud.py": "CRUD operations (UserRepository, PasswordRepository)",
            "__init__.py": "Package initialization",
        },
        "security": {
            "encryption.py": "Encryption/Decryption service (Fernet, PBKDF2)",
            "validators.py": "Input validation rules",
            "__init__.py": "Package initialization",
        },
        "services": {
            "auth.py": "Authentication business logic",
            "password.py": "Password management business logic",
            "__init__.py": "Package initialization",
        },
        "config.py": "Internal configuration",
        "utils.py": "Utility functions",
        "__init__.py": "Package initialization",
    },
    
    "tests": {
        "test_database.py": "Database tests",
        "test_validators.py": "Validator tests",
        "test_structure.py": "Structure tests",
        "__init__.py": "Test package initialization",
    },
    
    "scripts": {
        "init_db.py": "Database initialization script",
        "init_user.py": "User initialization script",
        "__init__.py": "Scripts package initialization",
    },
    
    "data": {
        "passwords.db": "SQLite database file (auto-created)",
    },
    
    "docs": {
        "ARCHITECTURE_NEW.md": "System architecture documentation",
        "CONTRIBUTING.md": "Contributing guidelines",
        "MIGRATION_GUIDE.md": "Migration guide",
        "PROJECT_COMPLETION_CHECKLIST.md": "Completion checklist",
        "REFACTORING_CHANGELOG.md": "Refactoring history",
    },
    
    "docs_and_info": {
        "_purpose": "Archived documentation and information files",
        "ARCHITECTURE.md": "Original architecture guide",
        "FINAL_SUMMARY.md": "Project summary",
        "FIXES_APPLIED.md": "Applied fixes and improvements",
        "PROJECT_INFO.py": "Project metadata",
        "PROJECT_STATS.txt": "Project statistics",
        "PROJECT_STATUS.md": "Detailed status",
        "PROJECT_SUMMARY.py": "Project summary script",
        "QUICKSTART.md": "Quick start guide",
        "README.md": "Original README",
        "pyproject.toml": "Build configuration",
        "requirements-dev.txt": "Development dependencies",
    },
    
    ".github": {
        "workflows": {
            "ci.yml": "GitHub Actions CI/CD pipeline",
        }
    },
    
    "directories": {
        ".venv": "Virtual environment (excluded from git)",
        "venv": "Alternative virtual environment",
        ".git": "Git repository",
        ".pytest_cache": "Pytest cache",
        "__pycache__": "Python cache (excluded from git)",
    }
}

FEATURES = {
    "Authentication": [
        "User registration with validation",
        "Secure login system",
        "Session management",
        "Password hashing with encryption",
        "Logout functionality",
    ],
    "Password Management": [
        "Add passwords with encryption",
        "View all saved passwords",
        "Update existing passwords",
        "Delete passwords",
        "Service categorization",
    ],
    "Security": [
        "AES-128 encryption (Fernet)",
        "PBKDF2-HMAC-SHA256 key derivation",
        "Unique salt per password",
        "No plain-text password storage",
        "Input validation",
    ],
    "Database": [
        "SQLite with proper schema",
        "Foreign key constraints",
        "Index optimization",
        "Automatic initialization",
    ],
    "Telegram Bot": [
        "Finite State Machine (FSM)",
        "Inline keyboards for selections",
        "Reply keyboards for actions",
        "Proper error handling",
        "User-friendly workflows",
    ],
    "Infrastructure": [
        "Modular architecture",
        "Service layer pattern",
        "Repository pattern",
        "Type hints",
        "Comprehensive logging",
    ],
}

TECHNOLOGY_STACK = {
    "Language": "Python 3.10+",
    "Framework": "aiogram 3.x",
    "Database": "SQLite3",
    "Encryption": "cryptography.fernet",
    "Key Derivation": "PBKDF2-HMAC-SHA256",
    "CI/CD": "GitHub Actions",
    "Testing": "pytest with coverage",
    "Code Quality": "flake8, pylint",
    "Security": "bandit, safety",
}

if __name__ == "__main__":
    print("Password Manager - Project Structure")
    print("=" * 50)
    print(f"\nRoot Files: {len(PROJECT_STRUCTURE['root_files'])} files")
    print(f"Features: {sum(len(v) for v in FEATURES.values())} features")
    print(f"Technology Stack: {len(TECHNOLOGY_STACK)} components")
