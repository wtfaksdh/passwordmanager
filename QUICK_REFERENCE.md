# Quick Reference Guide 📚

## Getting Started

### 1. Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env

# Add your Telegram Bot Token to .env
TELEGRAM_BOT_TOKEN=your_token_here
```

### 2. Run Application
```bash
python3 main.py
```

The bot will:
- Initialize the database (auto-create if needed)
- Start polling for Telegram updates
- Be ready to accept user commands

### 3. Bot Commands

#### Authentication
- `/start` - Begin or restart the bot
- `📝 Зарегистрироваться` - Register new account
- `🔓 Войти` - Login to existing account
- `🚪 Выход` - Logout

#### Password Management
- `➕ Добавить пароль` - Add new password
- `👁️ Просмотр паролей` - View all passwords
- `✏️ Обновить пароль` - Update password
- `🗑️ Удалить пароль` - Delete password

#### General
- `🚫 Отмена` - Cancel current action
- `⬅️ Назад` - Go back to previous menu

## File Structure

```
password_manager/
├── main.py                      # Start here
├── config.py                    # Configuration
├── requirements.txt             # Dependencies
├── README.md                    # Full documentation
├── STATUS.md                    # Project status
├── PROJECT_STRUCTURE.py         # This file
├── .env                         # Your environment vars
├── .env.example                 # Environment template
├── src/                         # Application code
│   ├── bot/                     # Telegram bot logic
│   ├── database/                # Database layer
│   ├── security/                # Encryption
│   └── services/                # Business logic
├── tests/                       # Unit tests
├── data/                        # Data storage
├── docs_and_info/               # Archived docs
└── .github/workflows/           # CI/CD pipelines
```

## Key Features

### Security
- 🔐 AES-128 encryption
- 🔑 PBKDF2 key derivation
- 🛡️ No plain-text storage
- ✓ Input validation

### User Experience
- 📱 Telegram bot interface
- ⌨️ Inline keyboards
- 💬 Clear error messages
- 🔄 Session management

## Development

### Running Tests
```bash
pytest tests/ -v --cov=src
```

### Code Quality
```bash
# Linting
flake8 src tests

# Static analysis
pylint src

# Security checks
bandit -r src
```

### CI/CD
- GitHub Actions automatically runs tests on push
- View workflow: `.github/workflows/ci.yml`

## Troubleshooting

### Bot doesn't start
- Verify `.env` has correct TELEGRAM_BOT_TOKEN
- Check internet connection
- Ensure Python 3.10+

### Database errors
- Delete `data/passwords.db` to reset
- App will reinitialize on next run

### Password issues
- Check username and password length
- Ensure special characters are valid
- Use Cancel button to restart

## Production Deployment

1. Use strong environment variables
2. Store `.env` securely (not in git)
3. Use PostgreSQL instead of SQLite
4. Enable HTTPS for API calls
5. Monitor logs and errors
6. Regular database backups

## More Information

- **Full Docs**: See `docs/` and `docs_and_info/`
- **Architecture**: `docs_and_info/ARCHITECTURE.md`
- **Status**: `STATUS.md`
- **Issues**: Fix list in `docs_and_info/FIXES_APPLIED.md`

---

**Need Help?** Check documentation files for detailed information.
