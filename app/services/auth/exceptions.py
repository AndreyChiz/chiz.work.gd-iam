from app.exceptions import BaseAppException, BaseErrorCode
from fastapi import status


class UserErrorCode(BaseErrorCode):
    unautorised = "Неверные данные автризации"
   
    


class UnautorisedException(BaseAppException):
    """Неавторизованный пользователь"""

    STATUS_CODE = status.HTTP_401_UNAUTHORIZED
    DETAIL = UserErrorCode.unautorised
