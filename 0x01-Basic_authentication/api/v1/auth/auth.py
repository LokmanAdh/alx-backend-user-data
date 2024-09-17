#!/usr/bin/env python3
""" Auth module """
from re import search
from typing import List, TypeVar

from flask import request


class Auth:
    """a class to manage the API authentication"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """returns True if the path is not in the list of excluded_paths"""
        if (path is None) or (excluded_paths is None or excluded_paths == []):
            return True
        for item in excluded_paths:
            if search(path, item):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """return the value of the header request"""
        authorization = request.headers.get('Authorization')
        if request and authorization:
            return authorization
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """returns None"""
        return None
