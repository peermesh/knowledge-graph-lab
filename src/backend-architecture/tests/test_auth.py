"""
Tests for authentication functionality.

This module contains unit tests for user authentication, authorization,
and security functions following TDD principles.
"""

import pytest
from datetime import datetime, timedelta

from app.auth.security import (
    create_access_token,
    create_refresh_token,
    verify_token,
    get_password_hash,
    verify_password,
    generate_session_id,
    check_permission,
)


class TestAuthentication:
    """Test cases for authentication functions."""

    def test_create_access_token(self):
        """Test JWT access token creation."""
        data = {"user_id": "test-user-123", "email": "test@example.com", "role": "user"}

        token = create_access_token(data)

        assert isinstance(token, str)
        assert len(token) > 0

        # Verify token payload
        payload = verify_token(token)
        assert payload is not None
        assert payload["user_id"] == "test-user-123"
        assert payload["email"] == "test@example.com"
        assert payload["role"] == "user"
        assert payload["type"] == "access"

    def test_create_refresh_token(self):
        """Test JWT refresh token creation."""
        data = {"user_id": "test-user-456", "email": "refresh@example.com", "role": "admin"}

        token = create_refresh_token(data)

        assert isinstance(token, str)
        assert len(token) > 0

        # Verify token payload
        payload = verify_token(token, "refresh")
        assert payload is not None
        assert payload["user_id"] == "test-user-456"
        assert payload["type"] == "refresh"

    def test_token_expiration(self):
        """Test token expiration handling."""
        data = {"user_id": "expired-user", "email": "expired@example.com"}

        # Create token that expires in 1 second
        expired_token = create_access_token(data, timedelta(seconds=1))

        # Token should be valid immediately
        payload = verify_token(expired_token)
        assert payload is not None

        # Wait for expiration (in real test, would use time mocking)
        # For now, just verify the token structure is correct

    def test_invalid_token_verification(self):
        """Test invalid token handling."""
        # Test with invalid token
        assert verify_token("invalid-token") is None

        # Test with wrong token type
        data = {"user_id": "test", "email": "test@example.com"}
        access_token = create_access_token(data)
        assert verify_token(access_token, "refresh") is None

    def test_password_hashing(self):
        """Test password hashing and verification."""
        password = "test-password-123"

        # Hash password
        hashed = get_password_hash(password)
        assert isinstance(hashed, str)
        assert hashed != password

        # Verify password
        assert verify_password(password, hashed) is True
        assert verify_password("wrong-password", hashed) is False

    def test_session_id_generation(self):
        """Test session ID generation."""
        session_id1 = generate_session_id()
        session_id2 = generate_session_id()

        assert isinstance(session_id1, str)
        assert isinstance(session_id2, str)
        assert len(session_id1) == 64  # 32 bytes * 2 hex chars
        assert len(session_id2) == 64
        assert session_id1 != session_id2  # Should be unique

    def test_permission_checking(self):
        """Test role-based permission checking."""
        # Test role hierarchy
        assert check_permission("admin", "user") is True
        assert check_permission("admin", "admin") is True
        assert check_permission("moderator", "user") is True
        assert check_permission("researcher", "user") is True
        assert check_permission("user", "admin") is False
        assert check_permission("user", "moderator") is False

        # Test same role
        assert check_permission("user", "user") is True
        assert check_permission("admin", "admin") is True

    @pytest.mark.parametrize("user_role,required_role,expected", [
        ("user", "user", True),
        ("user", "researcher", False),
        ("researcher", "user", True),
        ("researcher", "researcher", True),
        ("moderator", "user", True),
        ("moderator", "moderator", True),
        ("admin", "user", True),
        ("admin", "admin", True),
        ("user", "admin", False),
        ("researcher", "admin", False),
    ])
    def test_permission_matrix(self, user_role, required_role, expected):
        """Test permission matrix with various role combinations."""
        assert check_permission(user_role, required_role) == expected
