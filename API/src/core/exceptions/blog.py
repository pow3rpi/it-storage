from fastapi import HTTPException

from src.core.enums import ErrorEnum


class BlogValidationException(HTTPException):
    pass


class BlogLogicException(Exception):
    pass


class InvalidTitle(BlogValidationException):
    def __init__(self):
        super(InvalidTitle, self).__init__(
            status_code=422,
            detail=ErrorEnum[self.__class__.__name__].value
        )


class TooManyTags(BlogValidationException):
    def __init__(self):
        super(TooManyTags, self).__init__(
            status_code=422,
            detail=ErrorEnum[self.__class__.__name__].value
        )


class InvalidTag(BlogValidationException):
    def __init__(self):
        super(InvalidTag, self).__init__(
            status_code=422,
            detail=ErrorEnum[self.__class__.__name__].value
        )


class InvalidAnnotation(BlogValidationException):
    def __init__(self):
        super(InvalidAnnotation, self).__init__(
            status_code=422,
            detail=ErrorEnum[self.__class__.__name__].value
        )


class InvalidFileSize(BlogValidationException):
    def __init__(self):
        super(InvalidFileSize, self).__init__(
            status_code=422,
            detail=ErrorEnum[self.__class__.__name__].value
        )


class ContentNotFound(BlogLogicException):
    def __init__(self):
        super(ContentNotFound, self).__init__(
            ErrorEnum[self.__class__.__name__].value
        )
