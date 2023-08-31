#!/usr/bin/env python3
"""
module for handling password hashing
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
    return encoded string using bcrypt algorithm
    """
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    check if a password is valid
    """
    if bcrypt.checkpw(password.encode(), hashed_password):
        return True
    return False
