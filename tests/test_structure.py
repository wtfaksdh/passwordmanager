"""Tests for project structure and module imports"""
import sys
from pathlib import Path

# Add current directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))


def test_core_imports():
    """Test core module imports"""
    from src import (
        Database,
        DatabaseInitializer,
        User,
        Password,
        EncryptionService,
        Validators,
        AuthenticationService,
        PasswordService,
    )
    
    assert Database is not None
    assert DatabaseInitializer is not None
    assert User is not None
    assert Password is not None
    assert EncryptionService is not None
    assert Validators is not None
    assert AuthenticationService is not None
    assert PasswordService is not None


def test_encryption_service():
    """Test encryption and decryption"""
    from src.security import EncryptionService
    
    master_password = "test_user"
    password = "my_secure_password"
    
    # Encrypt
    encrypted = EncryptionService.encrypt_password(password, master_password)
    assert ":" in encrypted  # Should contain salt separator
    
    # Decrypt
    decrypted = EncryptionService.decrypt_password(encrypted, master_password)
    assert decrypted == password


def test_validators():
    """Test input validators"""
    from src.security import Validators
    
    # Valid username
    is_valid, msg = Validators.validate_username("valid_user")
    assert is_valid is True
    
    # Invalid username (too short)
    is_valid, msg = Validators.validate_username("ab")
    assert is_valid is False
    
    # Valid password
    is_valid, msg = Validators.validate_password("secure_pass")
    assert is_valid is True
    
    # Invalid password (too short)
    is_valid, msg = Validators.validate_password("123")
    assert is_valid is False


def test_interface_imports():
    """Test interface module imports"""
    from src.bot import (
        AuthStates,
        MainMenuStates,
        get_auth_keyboard,
        get_main_menu_keyboard,
    )
    
    assert AuthStates is not None
    assert MainMenuStates is not None
    assert get_auth_keyboard is not None
    assert get_main_menu_keyboard is not None


def test_config_imports():
    """Test configuration imports"""
    from config import (
        TELEGRAM_BOT_TOKEN,
        DB_PATH,
        LOG_LEVEL,
        WELCOME_MESSAGE,
        MAIN_MENU_MESSAGE,
    )
    
    assert WELCOME_MESSAGE is not None
    assert MAIN_MENU_MESSAGE is not None
    assert DB_PATH is not None


def test_main_imports():
    """Test main module can be imported"""
    import main
    assert main.main is not None
