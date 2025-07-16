from app.exceptions import BaseAppException, BaseErrorCode
from fastapi import status


class UserErrorCode(BaseErrorCode):
    unautorised = "Неверные данные автризации"
    unactive = "пользователь заблокирован"


class UnautorisedException(BaseAppException):
    """Неавторизованный пользователь"""

    STATUS_CODE = status.HTTP_401_UNAUTHORIZED
    DETAIL = UserErrorCode.unautorised


class UnactiveException(BaseAppException):
    """Неавторизованный пользователь"""

    STATUS_CODE = status.HTTP_403_FORBIDDEN
    DETAIL = UserErrorCode.unactive
