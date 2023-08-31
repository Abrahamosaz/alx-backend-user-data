#!/usr/bin/env python3
"""test filtered_logger function"""
import unittest
from parameterized import parameterized
from unittest.mock import patch
from typing import Tuple
from filtered_logger import filter_datum, RedactingFormatter


class TestFilterLogger(unittest.TestCase):

    @parameterized.expand([
        (("name", "age"), "rrr",  "age=32;name=abraham;school=uniben", ";"),
        (("school", "firstname"), "xxx",
         "age=32;firstname=abraham;school=uniben", ";")
    ])
    def test_filter_datum(
            self,
            fields: Tuple[str],
            redaction: str,
            message: str,
            sep: str):

        for field in fields:
            message = message.replace(field, redaction)
        self.assertEqual(filter_datum(
            fields, redaction, message, sep), message)
