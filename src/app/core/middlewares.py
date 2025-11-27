import random
import string
import time

from fastapi.exceptions import RequestValidationError
from loguru import logger
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.core.config import CONFIG


async def validation_exception_handler(
    _: Request, exc: RequestValidationError
) -> JSONResponse:
    validation_error_code = "InvalidRequest"
    message = ""
    for err in exc.errors():
        message += (
            f'Parameter: '
            f'{".".join(map(str, err["loc"][1:]))}, Error: {err["msg"]};'
        )
    logger.error(
        "Validation error: {} -> {}",
        validation_error_code,
        message.strip(),
    )
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"code": "InvalidRequest", "message": message.strip()},
    )


async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


async def log_requests(request: Request, call_next):
    rid = "".join(random.choices(string.ascii_uppercase + string.digits, k=16))
    request.state.request_id = rid

    start_time = time.time()

    with logger.contextualize(request_id=rid):
        try:
            response = await call_next(request)
        except Exception as e:
            logger.exception(f"Error processing request: {e}")
            if CONFIG.env == "PRODUCTION":
                response = JSONResponse(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    content="Something went wrong! Try again later",
                )
            else:
                raise

        elapsed = time.time() - start_time

        logger.info(
            "Method: '{method}' | "
            "URL : '{path}' | "
            "Status code: '{status_code}' | "
            "Response time: '{elapsed:.3f}s' ",
            method=request.method,
            path=request.url.path,
            elapsed=elapsed,
            status_code=response.status_code,
        )

        response.headers["X-Request-ID"] = rid

        return response
