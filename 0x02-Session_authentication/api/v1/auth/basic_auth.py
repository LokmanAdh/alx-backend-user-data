#!/usr/bin/env python3
""" Basic Auth"""
import base64
from re import search
from typing import TypeVar

from api.v1.auth.auth import Auth
from models.user import User


class BasicAuth(Auth):
    """inherits from Auth"""

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """returns the Base64 part of the Authorization header"""
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        header = authorization_header.replace("Basic ", "")
        return header

    def decode_base64_authorization_header(
        self, base64_authorization_header: str
    ) -> str:
        """returns the decoded value of a Base64 string"""
        if not base64_authorization_header:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            header_bytes = base64.b64decode(base64_authorization_header)
        except Exception as e:
            return None
        return header_bytes.decode("utf-8")

    def extract_user_credentials(
        self, decoded_base64_authorization_header: str
    ) -> (str, str):
        """returns the user email and password from the Base64 decoded value"""
        decoded = decoded_base64_authorization_header
        if decoded and isinstance(decoded, str) and ":" in decoded:
            res = decoded.split(":", 1)
            return (res[0], res[1])
        return (None, None)

    def user_object_from_credentials(
        self, user_email: str, user_pwd: str
    ) -> TypeVar("User"):
        """
        returns the User instance based on his email and password.
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        try:
            users = User.search({"email": user_email})
            if not users or users == []:
                return None
            for user in users:
                if user.is_valid_password(user_pwd):
                    return user
            return None
        except Exception:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ get the current user"""

        auth_header = self.authorization_header(request)
        if auth_header is not None:
            token = self.extract_base64_authorization_header(auth_header)
            if token is not None:
                decoded = self.decode_base64_authorization_header(token)
                if decoded is not None:
                    email, pwd = self.extract_user_credentials(decoded)
                    if email and pwd:
                        return self.user_object_from_credentials(email, pwd)
