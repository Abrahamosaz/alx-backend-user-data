#!/usr/bin/env python3
"""
BasicAuth class that inherit from Auth class
"""
from .auth import Auth
import base64
import binascii
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):

    def extract_base64_authorization_header(
        self,
        authorization_header: str
    ) -> str:
        """
        retrieve the Authorization header value from the request headers
        """
        try:
            assert authorization_header is not None
            assert isinstance(authorization_header, str)
            split_list = authorization_header.split(" ")
            if len(split_list) < 2 or split_list[0] != "Basic":
                raise AssertionError
            else:
                return authorization_header.split(" ")[1]
        except AssertionError:
            return None

    def decode_base64_authorization_header(
        self,
        base64_authorization_header: str
    ) -> str:
        """
        decode the base64 Authorization header value to string
        """
        try:
            assert base64_authorization_header is not None
            assert isinstance(base64_authorization_header, str)
            decoded_str = base64.b64decode(
                base64_authorization_header.encode("utf-8"))
            return decoded_str.decode("utf-8")
        except (AssertionError, binascii.Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str
    ) -> (str, str):
        """
        extract the user_email and user_paswword from the header
        Authorization
        """
        try:
            assert decoded_base64_authorization_header is not None
            assert isinstance(decoded_base64_authorization_header, str)
            if decoded_base64_authorization_header.find(":") == -1:
                raise AssertionError
        except AssertionError:
            return None, None

        decoded_value = decoded_base64_authorization_header.split(":")
        return decoded_value[0], decoded_value[1]

    def user_object_from_credentials(
            self,
            user_email: str,
            user_pwd: str
    ) -> TypeVar('User'):
        """
        return the user object from the user email and password
        """
        try:
            assert isinstance(user_email, str) and user_email is not None
            assert isinstance(user_pwd, str) and user_pwd is not None
            attr_dict = {"email": user_email}
            target_user_list = User.search(attr_dict)
            if len(target_user_list) == 0:
                raise AssertionError
            else:
                user_obj = target_user_list[0]
                if not user_obj.is_valid_password(user_pwd):
                    raise AssertionError
                else:
                    return user_obj
        except AssertionError:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        retrieve the current user object
        """
        auth_header = self.authorization_header(request)
        base64_header = self.extract_base64_authorization_header(auth_header)
        decode_b64_header = self.decode_base64_authorization_header(
            base64_header)
        user_email, user_pwd = self.extract_user_credentials(decode_b64_header)
        user_obj = self.user_object_from_credentials(user_email, user_pwd)
        return user_obj
