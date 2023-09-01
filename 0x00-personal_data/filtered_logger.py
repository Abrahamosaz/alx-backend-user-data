#!/usr/bin/env python3
""""
filtered_logger module
"""
from mysql.connector import connection
from typing import List
import logging
import re
import os


PII_FIELDS = ("name", "email", "phone", "password", "ssn")


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        message = super().format(record)
        return filter_datum(self.fields, self.REDACTION,
                            message, self.SEPARATOR)


def filter_datum(fields: List[str], redaction: str,
                 message: str,  seperator: str) -> str:
    """
    filter and replace value base on pattern defined
    """
    for s_w in fields:
        message = re.sub(
            r'(?<={v}=).+?{s}'.format(v=s_w, s=seperator),
            redaction, message)
    return message


def get_logger() -> logging.Logger:
    """function that create and return a new logger"""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    formatter = RedactingFormatter(PII_FIELDS)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    return logger


def get_db() -> connection.MySQLConnection:
    """return a msql.connector.connection.MySQLConnection object"""

    username = os.environ.get("PERSONAL_DATA_DB_USERNAME") or 'root'
    password = os.environ.get("PERSONAL_DATA_DB_PASSWORD") or ''
    host = os.environ.get("PERSONAL_DATA_DB_HOST") or 'localhost'
    db_name = os.environ.get("PERSONAL_DATA_DB_NAME")

    cnx = connection.MySQLConnection(
        username=username,
        passwd=password,
        host=host,
        database=db_name
    )
    return cnx


def main():
    """
    obtain db connnection and retrieve a the rows in the database
    and display using a specific format
    """
    logger = get_logger()
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users")
    field_names = cursor.column_names
    for row in cursor:
        message = "".join("{}={};".format(k, v)
                          for k, v in zip(field_names, row))
        logger.info(message.strip())
    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
