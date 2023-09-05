#!/usr/bin/env python3
"""
Module to handle the authentication system
"""
from flask import request
from typing import List, TypeVar


class Auth:

    def require_auth(self, path: str, excluded_path: List[str]) -> bool:
        """
        check if the request.path url need Authentication by using
        the excluded_path variable
        """
        try:
            assert path is not None
            assert excluded_path is not None or excluded_path != ""
        except AssertionError:
            return True

        path_str = ''
        if path != '/':
            path_str = path + '/'
        if path in excluded_path or path_str in excluded_path:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """
        return the  Authorization header value
        """
        try:
            assert request is not None
            assert request.headers.get("Authorization")
        except AssertionError:
            return None

        return request.headers.get("Authorization")

    def current_user(self, request=None) -> TypeVar('User'):
        """
        return the current user from the request object
        """
        return None
