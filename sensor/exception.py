import sys
import logging

def error_message_detail(error_message: str, error_detail: sys):
    _, _, exc_tb = error_detail.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename

    error_message = "Error occured python script name [{0}] line number[{1}] error message [{2}]".format(file_name, exc_tb.tb_lineno, error_message)
    return error_message


class SensorException(Exception):

    def __init__(self, error_message: str, error_detail: sys=sys):
        """
        :param error_message: custom error message in string format
        :param error_detail: custom error details which is instance of sys
        """
        super().__init__(error_message)

        self.error_message = error_message_detail(error_message, error_detail=error_detail)
        logging.error(self.error_message)
    def __str__(self):
        return self.error_message
