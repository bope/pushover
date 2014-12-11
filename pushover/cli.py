# coding: utf-8
import logging
import os
import sys

from pushover import Pushover
from pushover.utils import setup_argparser, setup_logger, parse_config

#: Module logger
log = logging.getLogger(__name__)

#: Default configuration path
DEFAULT_CONFIG = '~/.pushover.conf'


def main():
    """
    `pushover` command.
    """
    parser = setup_argparser('pushover')
    args = parser.parse_args()
    _ = setup_logger(args.verbosity)

    config_file = args.config_file
    if config_file:
        config_file = os.path.expanduser(config_file)
        if not os.path.isfile(config_file):
            log.error(u'Config file not found')
            sys.exit(1)
    else:
        config_file = os.path.expanduser(DEFAULT_CONFIG)
        if not os.path.isfile(config_file):
            config_file = None
            log.warning(u'Default config file not found')

    pushover = Pushover()

    if config_file:
        config = parse_config(config_file)
        users = config.get('users', {})
        apps = config.get('apps', {})

        for name, token in users.items():
            pushover.add_user(name, token)

        for name, token in apps.items():
            pushover.add_app(name, token)

    if args.message == '-':
        message = u''
        for line in sys.stdin:
            message += line
    else:
        message = args.message

    message_data = vars(args)

    if 'user_name' in message_data:
        message_data['user'] = message_data.pop('user_name')

    if 'app_name' in message_data:
        message_data['token'] = message_data.pop('app_name')

    message_data.pop('verbosity', None)
    message_data.pop('config_file', None)
    message_data.update(message=message)
    message_data = {k: v for k, v in message_data.items() if v}

    msg = pushover.message(**message_data)
    msg.validate_params()
    msg.send()


if __name__ == '__main__':
    try:
        main()
    except KeboardInterrupt:
        pass
