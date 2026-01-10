"""Test imports to verify project structure"""
import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))


def test_imports():
    """Test all imports"""
    print("Testing imports...")

    try:
        # Test config imports
        from src.config import TELEGRAM_BOT_TOKEN, States, BTN_REGISTER
        print("✅ config imports OK")

        # Test database imports
        from src.database.db import Database, init_db
        from src.database.models import User, Password
        from src.database.crud import UserCRUD, PasswordCRUD
        print("✅ database imports OK")

        # Test bot imports
        from src.bot.states import AuthStates, MainMenuStates
        from src.bot.keyboards import get_auth_keyboard, get_main_menu_keyboard
        from src.bot.handlers import router
        print("✅ bot imports OK")

        # Test utils imports
        from src.utils import is_valid_username, is_valid_password, is_valid_email
        print("✅ utils imports OK")

        print("\n✅ All imports successful!")
        return True

    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False


if __name__ == "__main__":
    success = test_imports()
    sys.exit(0 if success else 1)
