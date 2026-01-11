"""Tests for configuration and utilities"""
import pytest
from src.utils import is_valid_username, is_valid_password, is_valid_email


class TestValidators:
    """Test validator functions"""

    def test_is_valid_username_success(self):
        """Test valid usernames"""
        assert is_valid_username("john") is True
        assert is_valid_username("user123") is True
        assert is_valid_username("test_user") is True

    def test_is_valid_username_fail(self):
        """Test invalid usernames"""
        assert is_valid_username("ab") is False 
        assert is_valid_username("") is False 
        assert is_valid_username("user@name") is False 
        assert is_valid_username("user name") is False 

    def test_is_valid_password_success(self):
        """Test valid passwords"""
        assert is_valid_password("password123") is True
        assert is_valid_password("secret") is True

    def test_is_valid_password_fail(self):
        """Test invalid passwords"""
        assert is_valid_password("") is False 
        assert is_valid_password("abc") is False 

    def test_is_valid_email_success(self):
        """Test valid emails"""
        assert is_valid_email("user@example.com") is True
        assert is_valid_email("test.user@domain.co.uk") is True
        assert is_valid_email("name+tag@example.com") is True

    def test_is_valid_email_fail(self):
        """Test invalid emails"""
        assert is_valid_email("invalid.email") is False
        assert is_valid_email("user@") is False
        assert is_valid_email("@example.com") is False
        assert is_valid_email("") is False
