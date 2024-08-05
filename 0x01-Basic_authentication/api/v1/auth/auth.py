#!/usr/bin/env python3
"""defines of class Auth"""
from flask import request
from typing import (
    List,
    TypeVar
)


class Auth:
    """API authentication"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """determines whether a given path require authentication or not"""
        if path is None:
            return True
        elif excluded_paths is None or excluded_paths == []:
            return True
        elif path in excluded_paths:
            return False
        else:
            for e in excluded_paths:
                if e.startswith(path):
                    return False
                if path.startswith(e):
                    return False
                if e[-1] == "*":
                    if path.startswith(e[:-1]):
                        return False
        return True

    def authorization_header(self, request=None) -> str:
        """return authorization header from request object"""
        if request is None:
            return None
        header = request.headers.get('Authorization')
        if header is None:
            return None
        return header

    def current_user(self, request=None) -> TypeVar('User'):
        """return user instance from information from a request object"""
        return None
