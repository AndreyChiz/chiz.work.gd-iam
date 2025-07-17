from typing import Any

from fastapi import HTTPException, status




class ErrorCode:
    BASE_REG_USER_ERROR = ""
    #auth
    already_exist = "пользователь с такими данными существует"
    unautorised = "неверные данные автризации"
    unactive = "пользователь заблокирован"
    weak_password = "слабый пароль"
    not_found = "пользователь не найден"
    token_invalid = "невенрный accsess токен (прострочен)" #TODO убрать конкретику
    #user

    


class BaseAppException(HTTPException):
    STATUS_CODE = status.HTTP_500_INTERNAL_SERVER_ERROR
    DETAIL = ErrorCode.BASE_REG_USER_ERROR

    def __init__(self, **kwargs: dict[str, Any]) -> None:
        super().__init__(status_code=self.STATUS_CODE, detail=self.DETAIL, **kwargs)

# auth
class TokenInvalidException(BaseAppException):
    STATUS_CODE = status.HTTP_401_UNAUTHORIZED
    DETAIL = ErrorCode.token_invalid

class NotFoundException(BaseAppException):
    STATUS_CODE = status.HTTP_401_UNAUTHORIZED
    DETAIL = ErrorCode.not_found

class AlreadyExistException(BaseAppException):
    STATUS_CODE = status.HTTP_400_BAD_REQUEST
    DETAIL = ErrorCode.already_exist


class WeakPasswordError(BaseAppException):
    """Слабый праоль"""

    STATUS_CODE = status.HTTP_422_UNPROCESSABLE_ENTITY
    DETAIL = ErrorCode.weak_password


class UnautorisedException(BaseAppException):
    """Неавторизованный пользователь"""

    STATUS_CODE = status.HTTP_401_UNAUTHORIZED
    DETAIL = ErrorCode.unautorised


class UnactiveException(BaseAppException):
    """Неавторизованный пользователь"""

    STATUS_CODE = status.HTTP_403_FORBIDDEN
    DETAIL = ErrorCode.unactive
