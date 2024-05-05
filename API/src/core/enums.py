from enum import Enum, unique, IntEnum


@unique
class PostEnum(Enum):
    link = 'link'
    tutorial = 'tutorial'


@unique
class SearchEnum(Enum):
    link = PostEnum.link.value
    tutorial = PostEnum.tutorial.value
    all = 'all'


@unique
class ErrorEnum(IntEnum):
    UnknownError = 0
    InvalidUsername = 1
    UsernameExists = 2
    EmailExists = 3
    InvalidFirstname = 4
    InvalidLastname = 5
    InvalidPassword = 6
    PasswordsMismatch = 7
    InvalidCredentials = 8
    NonActivatedAccount = 9
    WrongPassword = 10
    EqualPasswords = 11
    InvalidToken = 12
    InvalidTitle = 13
    TooManyTags = 14
    InvalidTag = 15
    InvalidAnnotation = 16
    InvalidFileSize = 17
    ContentNotFound = 18


@unique
class APIHandlerEnum(Enum):
    SIGN_UP = 'SIGN UP'
    ACTIVATE_ACCOUNT = 'ACTIVATE ACCOUNT'
    LOG_IN = 'LOG IN'
    VERIFY_USER = 'VERIFY USER'
    LOG_OUT = 'LOG OUT'
    GET_ME = 'GET ME'
    UPDATE_PROFILE = 'UPDATE PROFILE'
    CHANGE_PASSWORD = 'CHANGE PASSWORD'
    CREATE_LINK = 'CREATE LINK'
    GET_LINK = 'GET LINK'
    UPDATE_LINK = 'UPDATE LINK'
    CREATE_TUTORIAL = 'CREATE TUTORIAL'
    GET_TUTORIAL = 'GET TUTORIAL'
    UPDATE_TUTORIAL = 'UPDATE TUTORIAL'
    GET_TAGS = 'GET TAGS'
    GET_POSTS = 'GET POSTS'
    DELETE_POST = 'DELETE POST'


@unique
class EmailTaskEnum(Enum):
    InitSignUpNotifyTask = 'InitSignUpNotifyTask'
    SignUpNotifySuccessTask = 'SignUpNotifySuccessTask'
    ChangePasswordNotifyTask = 'ChangePasswordNotifyTask'
