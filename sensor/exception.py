import sys

def error_message_detail(error, error_details:sys):
    """
    function to customize error message
    """
    _, _, exc_tb = error_details.exc_info()

    file_name = exc_tb.tb_frame.f_code.co_filename

    error_message = "Error occured in python script name [{0}], line_number [{1}], error_message [{2}]".format(
        file_name, exc_tb.tb_lineno, str(error)
    )

    return error_message


class SensorException(Exception):
    def __init__(self, error_message, error_details:sys):
        """
        Args:
            error_message : error message in string format
        """
        super().__init__(error_message)

        self.error_message = error_message_detail(error_message, error_details)

    def __str__(self):
        return self.error_message