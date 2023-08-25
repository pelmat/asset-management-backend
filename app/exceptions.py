from rest_framework.exceptions import APIException


class ExceptionMessage(APIException):
    pass


class TokenGenerationException(APIException):
    """Throw this error when token generation fails after 5 tries."""

    status_code = 404
    default_detail = 'Token generation failed after multiple retries. Please contact an administrator!'
