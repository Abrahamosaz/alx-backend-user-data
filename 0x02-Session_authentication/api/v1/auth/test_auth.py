#!/usr/bi/env python3
"""
Test auth methods both unittest and integrated tests
"""
import unittest
import unittest.mock
from unittest.mock import patch, MagicMock
from parameterized import parameterized
from .basic_auth import BasicAuth



class TestAuthMethods(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.test_obj = BasicAuth()

    @parameterized.expand([
        (None, None),
        (23, None),
        ("test", None),
        ("Basic Test", "Test"),
        ("Basic Value", "Value")
    ])
    def test_extract_auth_header(self, auth_header:str, expected_value: str):
        self.assertEqual(self.test_obj.extract_base64_authorization_header(auth_header), expected_value)

    @parameterized.expand([
        ("SG9sYmVydG9u", "TestResult"),
        (None, None),
        (23, None)
    ])
    def test_decode_base64(self, base64_auth: str, expected: str):
        attr = {"decode.return_value":  expected}
        with patch("base64.b64decode", return_value=MagicMock(**attr)):
            self.assertEqual(
                self.test_obj.decode_base64_authorization_header(base64_auth),
                expected)