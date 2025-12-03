from starlette import status

from app.exceptions.base import APIError
from app.exceptions.error_code import ErrorCode


class BadGatewayError(APIError):
    code = ErrorCode.BAD_GATEWAY
    status_code = status.HTTP_502_BAD_GATEWAY
    default_message = (
        "Error connecting to third party service. "
        "Please try again later."
    )


class AddressNotFoundError(APIError):
    code = ErrorCode.ADDRESS_NOT_FOUND
    default_message = "Address not found"
    status_code = status.HTTP_404_NOT_FOUND
