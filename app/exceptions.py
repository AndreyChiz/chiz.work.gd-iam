from typing import Any

from fastapi import HTTPException, status


class BaseErrorCode:
    BASE_REG_USER_ERROR = ""


class BaseAppException(HTTPException):
    STATUS_CODE = status.HTTP_500_INTERNAL_SERVER_ERROR
    DETAIL = BaseErrorCode.BASE_REG_USER_ERROR

    def __init__(self, **kwargs: dict[str, Any]) -> None:
        super().__init__(status_code=self.STATUS_CODE, detail=self.DETAIL, **kwargs)
