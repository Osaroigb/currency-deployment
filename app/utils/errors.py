import logging 
from .constants import *
logging.basicConfig(level=logging.ERROR)


class BaseError(Exception):
    def __init__(self, message:str, verboseMessage=None, errorType=None, httpCode=None):
        self.message = message or InternalServerErrorMessage
        self.verboseMessage = verboseMessage
        self.errorType = errorType or errorTypes['INTERNAL_SERVER_ERROR']
        self.httpCode = httpCode or statusCodes['500']

        logging.error(self.message)


class UnprocessableEntityError(BaseError):
    def __init__(self, message, verboseMessage=None, errorType=None):
        super().__init__(
            message= message or unprocessableEntityErrorMessage,
            httpCode= statusCodes["422"],
            errorType= errorType or errorTypes["UNPROCESSABLE_ENTITY"],
            verboseMessage=verboseMessage,
        )

class OperationForbiddenError(BaseError):
    def __init__(self, message:str, verboseMessage=None, errorType=None):
        super().__init__(
            message = message or operationForbiddenErrorMessage,
            httpCode= statusCodes["403"],
            errorType= errorType or errorType["OPERATION_FORBIDDEN"],
            verboseMessage=verboseMessage
        )

class NotFoundError(BaseError):
    def __init__(self, message: str, verboseMessage=None, errorType=None):
        super().__init__(
            message = message or notFoundErrorMessage,
            httpCode= statusCodes["404"],
            errorType=errorType or errorTypes["NOT_FOUND_ERROR"],
            verboseMessage=verboseMessage
        )

class InvalidCurrencyCode(BaseError):
    def __init__(self, message:str, verboseMessage=None):
        super().__init__(
            message=message or "Invalid currency code provided.",
            verboseMessage=verboseMessage,
            httpCode=statusCodes["400"],
            errorType=errorTypes["VALIDATION_FAILED"]
        )