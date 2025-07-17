from app.exceptions import BaseAppException, BaseErrorCode
from fastapi import status


class UserErrorCode(BaseErrorCode):
    already_exist = "пользователь с такими данными существует"
    unautorised = "Неверные данные автризации"
    unactive = "пользователь заблокирован"
    weak_password = "слабый пароль"


class AlreadyExistException(BaseAppException):
    STATUS_CODE = status.HTTP_400_BAD_REQUEST
    DETAIL = UserErrorCode.already_exist


class WeakPasswordError(BaseAppException):
    """Слабый праоль"""

    STATUS_CODE = status.HTTP_422_UNPROCESSABLE_ENTITY
    DETAIL = UserErrorCode.weak_password


class UnautorisedException(BaseAppException):
    """Неавторизованный пользователь"""

    STATUS_CODE = status.HTTP_401_UNAUTHORIZED
    DETAIL = UserErrorCode.unautorised


class UnactiveException(BaseAppException):
    """Неавторизованный пользователь"""

    STATUS_CODE = status.HTTP_403_FORBIDDEN
    DETAIL = UserErrorCode.unactive
