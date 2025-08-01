import sys
from src.logger import logging

def error_message_detail(error, error_detail):
    _, _, exc_tb = error_detail.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    line_number = exc_tb.tb_lineno
    return "Error occurred in Python script name [{0}] line number [{1}] error message [{2}]".format(
        file_name, line_number, str(error)
    )


class CustomException(Exception):
    def __init__(self, error_message, error_detail):
        super().__init__(error_message)
        self.error_message = error_message_detail(error_message, error_detail)
    def __str__(self):
        return self.error_message

"""
try:
    a = 1 / 0
except Exception as e:
    raise CustomException(e, sys)"""
