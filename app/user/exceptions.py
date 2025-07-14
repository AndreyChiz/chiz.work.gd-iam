from .external_deps import BaseAppException, BaseErrorCode  
from fastapi import status


class UserErrorCode(BaseErrorCode):
    USER_ALLREADY_EXIST = "User with this email or login already exist"


class UserAlreadyExist(BaseAppException):
    STATUS_CODE = status.HTTP_400_BAD_REQUEST
    DETAIL = UserErrorCode.USER_ALLREADY_EXIST

