# Password Manager Bot 🔐

Telegram-bot for secure password management with encryption.

## Quick Start

### Prerequisites
- Python 3.10+
- Telegram Bot Token

### Installation

```bash
pip install -r requirements.txt
```

### Configuration

1. Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

2. Add your Telegram Bot Token to `.env`:
```env
TELEGRAM_BOT_TOKEN=your_token_here
```

### Running

```bash
python3 main.py
```

## Features

✅ User registration with encrypted passwords  
✅ Secure login system  
✅ Add, view, update, and delete passwords  
✅ AES-128 encryption with PBKDF2-HMAC-SHA256  
✅ Session management  
✅ Input validation  

## Project Structure

```
├── main.py                 # Entry point
├── config.py               # Configuration
├── requirements.txt        # Dependencies
├── .env                    # Environment variables (create from .env.example)
├── .env.example            # Environment template
├── src/
│   ├── bot/               # Telegram bot handlers
│   ├── database/          # Database layer
│   ├── security/          # Encryption & validation
│   └── services/          # Business logic
├── tests/                 # Unit tests
├── data/                  # Data directory
└── .github/workflows/     # CI/CD pipelines
```

## Security

🔒 All passwords encrypted with Fernet (AES-128)  
🔒 Master password-based key derivation  
🔒 Unique salt for each password  
🔒 PBKDF2 with 100,000 iterations  

## Documentation

See `docs_and_info/` folder for detailed documentation including:
- Architecture guide
- Project status
- Fixes applied

## CI/CD

Automated testing and security checks on every push via GitHub Actions.

---

For more information, see documentation in `docs_and_info/` folder.
