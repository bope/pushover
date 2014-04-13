pushover
========

A simple python pushover module / CLI

CLI
===

    $ pushover -a <app-name> -u <user-name> -m <message>
    $ pushover -A <app-token> -U <user-token> -m <message>
    $ echo "message" | pushover -a <app-name> -u <user-name> -s <sound> -t <title>

Arguments:

    $ pushover -h
    usage: pushover [-h] [-c CONFIG_FILE] [-v] [-u USER_NAME] [-U USER]
                    [-a APP_NAME] [-A TOKEN] [-d DEVICE] [-p PRIORITY] [-l URL]
                    [-L URL_TITLE] [-t TITLE] [-s SOUND] [-m MESSAGE]
    
    optional arguments:
      -h, --help            show this help message and exit
      -c CONFIG_FILE, --config CONFIG_FILE
      -v, --verbose
      -u USER_NAME, --user USER_NAME
      -U USER, --user-token USER
      -a APP_NAME, --app APP_NAME
      -A TOKEN, --app-token TOKEN
      -d DEVICE, --device DEVICE
      -p PRIORITY, --priority PRIORITY
      -l URL, --url URL
      -L URL_TITLE, --url-title URL_TITLE
      -t TITLE, --title TITLE
      -s SOUND, --sound SOUND
      -m MESSAGE, --message MESSAGE


To use usernames and application names intead of tokens, use a configuration
file (`~/.pushover.conf`).

    users:
      <username1>: <user token1>
      <username2>: <user token2>

    apps:
      <application name1>: <application token1>
      <application name1>: <application token2>


pushover module
===============

Messaging:

    >>> import pushover
    >>> m = pushover.Message(token='<app token>', user='<user token>', message='text')
    >>> m
    {'message': 'text', 'user': '<user token>', 'token': '<app token>'}
    >>> m.send()
    (True, {u'status': 1, u'request': u'<message token>'})

User / Apps:

    >>> import pushover
    >>> p = pushover.Pushover()
    >>> p.add_user('per', '<user token>')
    >>> p.add_app('test', '<apptoken>')
    >>> m = p.message('per', 'test', 'text')
    >>> m
    {'message': 'text', 'user': <User per>, 'token': <App test>}
    >>> m.user
    <User per>
    >>> m.message = 'new message'
    >>> m
    {'message': 'new message', 'user': <User per>, 'token': <App test>}
    >>> m['message'] = 'another message'
    >>> m
    {'message': 'another message', 'user': <User per>, 'token': <App test>}
    >>> m.update(sound='spacealarm')
    >>> m
    {'sound': 'spacealarm', 'message': 'another message', 'user': <User per>, 'token': <App test>}
    >>> m.send()
    (True, {u'status': 1, u'request': u'<message token>'})