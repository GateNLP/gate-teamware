from django.test import TestCase
from django.core import mail

from django.core.mail.backends.smtp import EmailBackend as SMTPBackend
from django.core.mail.backends.console import EmailBackend as ConsoleBackend

class TestEmailBackend(TestCase):

    def test_email_console_backend(self):
        cbackend = ConsoleBackend()

        mail.send_mail(subject="Test subject",
                       message="Message content",
                       from_email="from@from.com",
                       recipient_list=["to@to.com"],
                       connection=cbackend)


