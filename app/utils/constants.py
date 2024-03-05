InternalServerErrorMessage = "Error occured during operation. We're currently checking why this happend."
unprocessableEntityErrorMessage="Unprocessable Entity. Error during payload Validation."
httpErrorMessage="Error occured during operation. Please try again later."
serviceUnavailableErrorMessage="Error occured during operation. Please try again later.",
operationForbiddenErrorMessage= "Operation forbidden",
notFoundErrorMessage="No user record found with this email! Please signup first.",

errorTypes = {
    "HTTP_ERROR": 'HTTP_ERROR',
    "HTTP_CONNECTION_ERROR": 'HTTP_CONNECTION_ERROR',
    "INTERNAL_SERVER_ERROR": 'INTERNAL_SERVER_ERROR',
    "UNPROCESSABLE_ENTITY": 'UNPROCESSABLE_ENTITY',
    "VALIDATION_FAILED": "VALIDATION_FAILED",
    "OPERATION_FORBIDDEN": 'OPERATION_FORBIDDEN',
    "NOT_FOUND_ERROR": 'NOT_FOUND_ERROR',
}

statusCodes = {
    "200":200,
    "201":201,
    "400":400,
    "401":401,
    "422":422,
    "500":500,
    "403":403,
    "404":404
}