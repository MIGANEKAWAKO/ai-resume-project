from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from fastapi import Request
from fastapi.exceptions import RequestValidationError


class ResumeParseError(HTTPException):
    def __init__(self, detail: str = "Failed to parse resume PDF"):
        super().__init__(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=detail)


class FileTooLargeError(HTTPException):
    def __init__(self, max_mb: int = 10):
        super().__init__(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File exceeds maximum allowed size of {max_mb} MB",
        )


class InvalidFileTypeError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are accepted",
        )


class ResumeNotFoundError(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found")


class AIExtractionError(HTTPException):
    def __init__(self, detail: str = "AI model failed to extract information"):
        super().__init__(status_code=status.HTTP_502_BAD_GATEWAY, detail=detail)


async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    if isinstance(exc, RequestValidationError):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"detail": f"请求参数校验失败：{exc.errors()}"},
        )
    if isinstance(exc, HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
        )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "服务器内部错误"},
    )
