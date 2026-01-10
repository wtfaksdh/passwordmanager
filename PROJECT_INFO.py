pyproject = "password-manager"
version = "0.1.0"
description = """
Password Manager with Telegram Bot Interface and SQLite3 Database.
A simple yet powerful tool to manage passwords securely through Telegram.
"""

features = [
    "User registration and authentication",
    "CRUD operations for passwords",
    "SQLite3 database",
    "Telegram bot interface with FSM",
    "User-friendly keyboard navigation",
    "Password management per service",
]

architecture = {
    "database": "SQLite3 with users and passwords tables",
    "bot": "Telegram aiogram 3.x with FSM states",
    "validation": "Input validation for usernames, passwords, emails",
    "testing": "Unit tests with pytest and coverage reports",
    "ci_cd": "GitHub Actions with multi-version testing",
}

python_version = ">=3.9"

main_dependencies = [
    "aiogram==3.24.0",
    "aiohttp==3.13.3",
    "aiofiles==23.2.1",
    "python-dotenv==1.2.1",
    "pydantic==2.9.2",
]

dev_dependencies = [
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
    "black>=23.0.0",
    "flake8>=6.0.0",
    "mypy>=1.0.0",
]

project_structure = """
passwordmanager/
├── src/
│   ├── bot/              # Telegram bot implementation
│   │   ├── handlers.py   # Command handlers
│   │   ├── states.py     # FSM states
│   │   └── keyboards.py  # UI keyboards
│   ├── database/         # Database layer
│   │   ├── models.py     # Data models
│   │   ├── db.py         # DB initialization
│   │   └── crud.py       # CRUD operations
│   ├── config.py         # Configuration
│   └── utils.py          # Utilities
├── tests/                # Test suite
│   ├── test_database.py  # Database tests
│   └── test_validators.py # Validator tests
├── scripts/              # Helper scripts
│   └── init_db.py        # Database initialization
├── .github/workflows/    # CI/CD
│   └── ci.yml            # GitHub Actions
├── main.py               # Entry point
├── pyproject.toml        # Project config
├── requirements.txt      # Dependencies
└── README.md             # Documentation
"""

quick_start_steps = [
    "1. Clone the repository",
    "2. Create virtual environment: python3 -m venv venv",
    "3. Activate it: source venv/bin/activate",
    "4. Install deps: pip install -r requirements.txt",
    "5. Set TELEGRAM_BOT_TOKEN in .env",
    "6. Run: python3 main.py",
]

testing = {
    "unit_tests": "pytest tests/ -v",
    "coverage": "pytest tests/ --cov=src",
    "lint": "flake8 src/ tests/",
    "format": "black src/ tests/",
    "types": "mypy src/",
}

security_notes = """
⚠️ Important:
- Passwords are stored in plain text in SQLite3
- For production use, add encryption with cryptography library
- Implement proper authentication and session management
- Use HTTPS for API communications
- Add logging and monitoring
"""

license = "MIT"
author = "Your Name"
email = "your.email@example.com"
