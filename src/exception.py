import sys, os
import logging

#function for how your message look like
def error_message_details(error, error_detail:sys):
    _, _, exc_tb = error_detail.exc_info()  #it will give 3 data i need only last one
    file_name = exc_tb.tb_frame.f_code.co_filename
    error_message = f"Error occured in python script name {file_name} line number {exc_tb.tb_lineno} error message {str(error)}"

    return error_message

#construct the class which inherit from Exception 
class CustomException(Exception):
    def __init__(self, error_message, error_detail:sys):
        super().__init__(error_message) 
        self.error_message = error_message_details(error_message, error_detail=error_detail)

# print the error message
    def __str__(self) -> str:
        return self.error_message
    

if __name__ == "__main__":
    try:
        a = 1/0
    except Exception as e:
        
        logging.info("ZeroDivisionError")
        raise CustomException (e, sys)