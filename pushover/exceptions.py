# coding: utf-8


class PushoverException(Exception):
    """
    Base exception for Pushover module.
    """
    pass


class MissingParam(PushoverException):
    """
    Raised when Message parameter is missing.
    """
    pass


class UnknownParam(PushoverException):
    """
    Raised when unknown parameter is supplied to Message.
    """
    pass


class ApplicationNotFound(PushoverException):
    """
    Raised when unknowns application is accessed by name.
    """
    pass


class UserNotFound(PushoverException):
    """
    Raised when unknown user is accessed by name.
    """
    pass


class ValidationError(PushoverException):
    """
    Raised when message parameter is invalid.
    """
    pass
