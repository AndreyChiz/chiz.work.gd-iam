from typing import Any

from fastapi import HTTPException, status


class BaseAppException(HTTPException):
    """Base description call developer"""

    STATUS_CODE = status.HTTP_500_INTERNAL_SERVER_ERROR

    def __init__(self, **kwargs: dict[str, Any]) -> None:
        detail = self.__class__.__doc__ or "No description, call developer"
        super().__init__(status_code=self.STATUS_CODE, detail=detail, **kwargs)


# auth
class AccessTokenInvalidException(BaseAppException):
    """невенрный accsess токен"""

    STATUS_CODE = status.HTTP_401_UNAUTHORIZED


class RefreshTokenInvalidException(BaseAppException):
    """невенрный refresh токен"""
    STATUS_CODE = status.HTTP_401_UNAUTHORIZED

class RefreshTokenExpireException(BaseAppException):
    """просрочен refresh токен"""
    STATUS_CODE = status.HTTP_401_UNAUTHORIZED


class NotFoundException(BaseAppException):
    """пользователь не найден"""

    STATUS_CODE = status.HTTP_401_UNAUTHORIZED


class AlreadyExistException(BaseAppException):
    """Пользователь с такими данными существует"""

    STATUS_CODE = status.HTTP_400_BAD_REQUEST


class WeakPasswordError(BaseAppException):
    """Слабый праоль"""

    STATUS_CODE = status.HTTP_422_UNPROCESSABLE_ENTITY


class UnautorisedException(BaseAppException):
    """Неавторизованный пользователь"""

    STATUS_CODE = status.HTTP_401_UNAUTHORIZED


class UnactiveException(BaseAppException):
    """Заблокированный пользователь"""

    STATUS_CODE = status.HTTP_403_FORBIDDEN


class NoRefreshToken(BaseAppException):
    """Отсутствует refresh токен"""

    STATUS_CODE = status.HTTP_401_UNAUTHORIZED
