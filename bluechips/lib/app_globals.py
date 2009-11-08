"""The application's Globals object"""

import logging

from pylons import config, request
from paste.deploy.converters import asbool
from mailer import Message

log = logging.getLogger(__name__)

class Globals(object):
    """Globals acts as a container for objects available throughout the
    life of the application
    """

    def __init__(self):
        """One instance of Globals is created during application
        initialization and is available during requests via the 'g'
        variable
        """
        pass

    def send_message(self, msg):
        """
        Wrap the call to mailer.send() so that we can do stuff like defer mail
        sending, wrap in a test fixture, selectively disable mailing in certain
        environments, etc.
        """
        if asbool(config.get('testing')) or asbool(config.get('network_free')):
            if 'mailer.messages' not in request.environ:
                request.environ['mailer.messages'] = []
            request.environ['mailer.messages'].append(msg)
            log.info("From: %s\nTo: %s\nSubject: %s\n\n%s",
                     msg.From, msg.To, msg.Subject, msg.Body)
        else:
            self.mailer.send(msg) # pragma: nocover

    def handle_notification(self, users, subject, body):
        "Send a notification email."
        recipients = [u.email for u in users if u.email is not None]
        if len(recipients) > 0:
            msg = Message(From=config.get('mailer.from',
                                          'root@localhost'),
                          To=recipients)
            msg.Subject = "BlueChips: %s" % subject
            msg.Body = body
            self.send_message(msg)
