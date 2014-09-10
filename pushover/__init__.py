# coding: utf-8
import logging

from pushover.utils import message, translate_params, validate, NamedToken
from pushover.exceptions import (MissingParam, UnknownParam, ValidationError,
                                 ApplicationNotFound, UserNotFound)

#: Module logger
log = logging.getLogger(__name__)

#: Available message params
AVAILABLE_PARAMS = [
    'token',
    'user',
    'message',
    'device',
    'title',
    'url',
    'url_title',
    'priority',
    'timestamp',
    'sound',
]

#: Required message params
REQUIRED_PARAMS = [
    'token',
    'user',
    'message'
]


class Message(dict):
    """
    Message representation as a dictionary.
    """
    def __init__(self, token, user, message, **kwargs):
        """
        :param token: Application token
        :type token: str
        :param user: User token
        :type user: str
        :param message: Message text
        :type message: str
        :param **kwargs: Additional message fields
        """
        kwargs.update(
            token=token,
            user=user,
            message=message,
        )
        kwargs = {k: v for k, v in kwargs.items()}
        super(Message, self).__init__(**kwargs)

    def __getattr__(self, item):
        try:
            return self[item]
        except KeyError:
            raise AttributeError

    def __setattr__(self, key, value):
        self[key] = value

    def validate_params(self):
        """
        Make sure message is sendable.
        """
        for req in REQUIRED_PARAMS:
            if req not in self:
                raise MissingParam(u'Required param %s missing' % req)

        for key in self:
            if key not in AVAILABLE_PARAMS:
                raise UnknownParam(u'Param %s not available')

        message = self.get('message', '')
        title = self.get('title', '')
        url = self.get('url', '')
        url_title = self.get('url_title', '')
        priority = self.get('priority', 0)

        if (len(message) + len(title)) > 512:
            raise ValidationError(u'Message and/or title is too long')

        if len(url) > 500:
            raise ValidationError(u'URL is too long')

        if len(url_title) > 50:
            raise ValidationError(u'URL title is too long')

        try:
            priority = int(priority)
        except ValueError:
            raise ValidationError(u'Priority must be an int')

        if -1 >= priority >= 2:
            raise ValidationError(u'Priority must be between -1 and 2')

    def send(self):
        """
        Send message.

        :returns: (Success, Response):
        :rtype: (bool, dict)
        """
        log.info(u'sending message: %s', self)
        return message(**translate_params(self))


class User(NamedToken):
    """
    User token object.
    """
    def message(self, **kwargs):
        """
        Create message for user.
        :param **kwargs: Message fields, see :py:class:`Message`
        :returns: Message instance
        :rtype: :py:class:`Message`
        """
        return Message(user=self, **kwargs)


class App(NamedToken):
    """
    Application token object.
    """
    def message(self, **kwargs):
        """
        Create message from application.
        :param **kwargs: Message fields
        :returns: :py:class:`Message`
        """
        return Message(token=self, **kwargs)


class Pushover(object):
    """
    Collection of registered users and application.
    """
    def __init__(self):
        self.users = {}
        self.apps = {}

    def add_user(self, username, token):
        """
        Add a user by name and token.

        :param username: Username used to refer to user
        :type username: str
        :param token: User token
        :type token: str
        """
        self.users[username] = User(username, token)

    def add_app(self, appname, token):
        """
        Add application by name and token.

        :param appname: Application name
        :type appname: str
        :param token: Application token
        :type token: str
        """
        self.apps[appname] = App(appname, token)

    def validate(self, token, user, device=None):
        """
        Verify user.

        :param token: Application token or names
        :type token: str
        :param user: User token or name
        :type user: str
        :param device: User device
        :type device: str
        :returns: Success, validation status
        :rtype: bool, bool
        """
        token = self.apps.get(token, token)
        user = self.users.get(user, user)
        params = {
            'token': token,
            'user': user
        }

        if device:
            params.update(device=device)

        return validate(**translate_params(params))

    def message(self, user, token, message, **kwargs):
        """
        Create message from application for user

        :param user: User token or name
        :type user: str
        :param token: Application token or name
        :type token: str
        :param message: Message text
        :type message: str
        :param **kwargs: Additional message fields
        :returns: Message instance
        :rtype: :py:class:`Message`
        """
        app_obj = self.apps.get(token, None)
        user_obj = self.users.get(user, None)

        if not app_obj and not user_obj:
            return Message(token=token, user=user, message=message, **kwargs)

        if app_obj:
            return app_obj.message(user=user_obj, message=message, **kwargs)

        return user_obj.message(token=token, message=message, **kwargs)

    def send(self, *args, **kwargs):
        """
        Shortcut for sending message. Arguments are the same as for
        :py:meth:`Pushover.message`.

        :returns: Success, response
        :rtype: (bool, dict)
        """
        return self.message(*args, **kwargs).send()
