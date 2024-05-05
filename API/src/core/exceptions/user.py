from fastapi import HTTPException

from src.core.enums import ErrorEnum


class AuthValidationException(HTTPException):
    pass


class AuthLogicException(Exception):
    pass


class InvalidUsername(AuthValidationException):
    def __init__(self):
        super(InvalidUsername, self).__init__(
            status_code=422,
            detail=ErrorEnum[self.__class__.__name__].value
        )


class UsernameExists(AuthLogicException):
    def __init__(self):
        super(UsernameExists, self).__init__(
            ErrorEnum[self.__class__.__name__].value
        )


class EmailExists(AuthLogicException):
    def __init__(self):
        super(EmailExists, self).__init__(
            ErrorEnum[self.__class__.__name__].value
        )


class InvalidFirstname(AuthValidationException):
    def __init__(self):
        super(InvalidFirstname, self).__init__(
            status_code=422,
            detail=ErrorEnum[self.__class__.__name__].value
        )


class InvalidLastname(AuthValidationException):
    def __init__(self):
        super(InvalidLastname, self).__init__(
            status_code=422,
            detail=ErrorEnum[self.__class__.__name__].value
        )


class InvalidPassword(AuthValidationException):
    def __init__(self):
        super(InvalidPassword, self).__init__(
            status_code=422,
            detail=ErrorEnum[self.__class__.__name__].value
        )


class PasswordsMismatch(AuthValidationException):
    def __init__(self):
        super(PasswordsMismatch, self).__init__(
            status_code=422,
            detail=ErrorEnum[self.__class__.__name__].value
        )


class InvalidVerificationLink(AuthLogicException):
    def __init__(self):
        super(InvalidVerificationLink, self).__init__(
            ErrorEnum[self.__class__.__name__].value
        )


class InvalidCredentials(AuthLogicException):
    def __init__(self):
        super(InvalidCredentials, self).__init__(
            ErrorEnum[self.__class__.__name__].value
        )


class NonActivatedAccount(AuthLogicException):
    def __init__(self):
        super(NonActivatedAccount, self).__init__(
            ErrorEnum[self.__class__.__name__].value
        )


class WrongPassword(AuthLogicException):
    def __init__(self):
        super(WrongPassword, self).__init__(
            ErrorEnum[self.__class__.__name__].value
        )


class EqualPasswords(AuthLogicException):
    def __init__(self):
        super(EqualPasswords, self).__init__(
            ErrorEnum[self.__class__.__name__].value
        )


class InvalidToken(AuthLogicException):
    def __init__(self):
        super(InvalidToken, self).__init__(
            ErrorEnum[self.__class__.__name__].value
        )
