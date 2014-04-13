# coding: utf-8


class PushoverException(Exception):
    pass


class MissingParam(PushoverException):
    pass


class UnknownParam(PushoverException):
    pass


class ApplicationNotFound(PushoverException):
    pass


class UserNotFound(PushoverException):
    pass


class ValidationError(PushoverException):
    pass
