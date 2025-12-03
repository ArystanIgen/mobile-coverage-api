from starlette.exceptions import HTTPException

from app.exceptions.error_code import ErrorCode


class APIError(HTTPException):
    __slots__ = ("code", "message")

    code: ErrorCode
    status_code: int
    default_message: str = ""

    def __init__(self, message: str | None = None):
        message = message or self.default_message
        self.message = message

        super().__init__(status_code=self.status_code, detail=message)

    @property
    def payload(self) -> dict[str, str]:
        return {
            "code": self.code.value,
            "message": self.message,
        }
