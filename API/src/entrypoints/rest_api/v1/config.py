from fastapi import HTTPException

from src.core.enums import ErrorEnum

UnknownErrorException = HTTPException(
    status_code=400,
    detail=ErrorEnum.UnknownError.value
)
