#!/usr/bin/env python3
"""defines a hash_password function"""
import bcrypt
from bcrypt import hashpw


def hash_password(password: str) -> bytes:
    """return the password"""
    p = password.encode()
    hashed = hashpw(p, bcrypt.gensalt())
    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """see whether a password is valid"""
    return bcrypt.checkpw(password.encode(), hashed_password)
