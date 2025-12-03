from enum import StrEnum


class ErrorCode(StrEnum):
    FORBIDDEN = "Forbidden"
    BAD_GATEWAY = "BadGateway"
    INVALID_REQUEST = "InvalidRequest"
    ADDRESS_NOT_FOUND = "AddressNotFound"
