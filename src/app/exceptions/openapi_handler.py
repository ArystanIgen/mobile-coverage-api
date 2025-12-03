from typing import Any
from pydantic import BaseModel


class Message(BaseModel):
    code: str
    message: str


def openapi_handle_error(*args) -> dict[int | str, dict[str, Any]] | None:
    errors_dict = {}
    for error in args:
        error_dict = error().payload
        errors_dict[error().status_code] = {
            "model": Message,
            "description": error_dict["message"],
        }
    return errors_dict
