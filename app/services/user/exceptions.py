from app.exceptions import BaseAppException, BaseErrorCode  
from fastapi import status


class UserErrorCode(BaseErrorCode):
    USER_ALLREADY_EXIST = "Пользователь с такими данными уже существует"
    WEAK_PASSWORD = (
            "Пароль должен содержать хотя бы одну цифру и один специальный символ (!, _, @, #, $, %, ^, &, *), "
            "а также состоять только из латинских букв, цифр и допустимых спецсимволов. "
            "Длина — от 6 до 128 символов."
    )

class UserAlreadyExist(BaseAppException):
    STATUS_CODE = status.HTTP_400_BAD_REQUEST
    DETAIL = UserErrorCode.USER_ALLREADY_EXIST
