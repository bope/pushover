# coding: utf-8
from __future__ import with_statement
import logging

import requests
import yaml
import argparse


API_URL = u'https://api.pushover.net/1'
API_MESSAGE_URL = u'%s/messages.json' % API_URL
API_VALIDATE_URL = u'%s/validate.json' % API_URL

#: Log levels for CLI
LOG_LEVELS = [
    logging.ERROR,
    logging.WARNING,
    logging.INFO,
    logging.DEBUG,
]

LOG_FORMAT = u'%(asctime)s %(levelname)s %(name)s %(message)s'


class NamedToken(object):
    """
    Name to token mapping. Used for user and application registration.
    """
    def __init__(self, name, token):
        """
        :param name: Field name used for token
        :param token: Token value
        """
        self.name = name
        self.token = token

    def message(self, **kwargs):
        raise NotImplementedError

    def __repr__(self):
        return '<%s %s>' % (self.__class__.__name__, self.name)


def message(**kwargs):
    """
    Send message to pushover API.

    :param **kwargs: Request data
    :returns: (Success bool, Response dict)
    """
    res = requests.post(API_MESSAGE_URL, params=kwargs)
    return res.ok, res.json()


def validate(**kwargs):
    """
    Send validation request to oushover API.

    :param **kwargs: Request data
    :returns: (Success bool, Validation status)
    """
    res = requests.post(API_VALIDATE_URL, params=kwargs)
    return res.ok, bool(res.json().get('status', False))


def translate_params(kwargs):
    """
    Translate named tokens to field and values.

    :param kwargs: Params dict
    :returns: Dict
    """
    ret = kwargs.copy()
    for key, value in ret.items():
        if isinstance(value, NamedToken):
            ret[key] = value.token
    return ret


def setup_logger(verbosity):
    """
    Create logger for CLI command.

    :param verbosity: Log level index for `LOG_LEVELS`
    :returns: :py:class:`logging.Logger`
    """
    try:
        log_level = LOG_LEVELS[verbosity]
    except IndexError:
        log_level = LOG_LEVELS[-1]

    r = logging.getLogger('requests')
    r.setLevel(logging.ERROR)

    logger = logging.getLogger()
    logger.setLevel(log_level)
    handler = logging.StreamHandler()
    handler.setLevel(log_level)
    formatter = logging.Formatter(LOG_FORMAT)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


def setup_argparser(prog):
    """
    Create CLI argument parser.

    :param prog: Program name
    :returns: :py:class:`argparse.ArgumentParser`
    """
    parser = argparse.ArgumentParser(prog)
    parser.add_argument('-c', '--config', dest='config_file', default=None)
    parser.add_argument('-v', '--verbose', dest='verbosity', action='count',
                        default=0)
    parser.add_argument('-u', '--user', dest='user_name', default=None)
    parser.add_argument('-U', '--user-token', dest='user', default=None)
    parser.add_argument('-a', '--app', dest='app_name', default=None)
    parser.add_argument('-A', '--app-token', dest='token', default=None)
    parser.add_argument('-d', '--device', dest='device', default=None)
    parser.add_argument('-p', '--priority', dest='priority', default=None)
    parser.add_argument('-l', '--url', dest='url', default=None)
    parser.add_argument('-L', '--url-title', dest='url_title', default=None)
    parser.add_argument('-t', '--title', dest='title', default=None)
    parser.add_argument('-s', '--sound', dest='sound', default=None)
    parser.add_argument('-m', '--message', dest='message', default='-')

    return parser


def parse_config(filepath):
    """
    Parse config file.

    :param filepath: Path to configuration file
    :returns: Dict
    """
    with open(filepath, 'r') as fh:
        return yaml.safe_load(fh.read())