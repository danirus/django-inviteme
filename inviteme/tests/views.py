import re
import threading

from django.conf import settings
from django.core import mail
from django.core.urlresolvers import reverse
from django.test import TestCase

from inviteme import signals, signed
from inviteme.models import ContactMail
from inviteme.views import INVITEME_SALT
from inviteme.utils import mail_sent_queue


class GetFormViewTestCase(TestCase):

    def test_get_form(self):
        response = self.client.get(reverse("inviteme-get-form"))
        # Check whether the form has all expected fields
        self.assertContains(response, 'name="timestamp"')
        self.assertContains(response, 'name="security_hash"')
        self.assertContains(response, 'name="honeypot"')
        self.assertContains(response, 'name="email"')


class PostFormViewTestCase(TestCase):
  
    def setUp(self):
        self.response = self.client.get(reverse("inviteme-get-form"))
        for context in self.response.context:
            if context.has_key("form"):
                form = context.get("form")
                self.timestamp = form.initial["timestamp"]
                self.security_hash = form.initial["security_hash"]

    def post_valid_data(self):
        data = {'timestamp':     self.timestamp,
                'security_hash': self.security_hash,
                'email':         'alice.bloggs@example.com' }
        self.response = self.client.post(
            reverse("inviteme-post-form"), data=data)        
  
    def test_post_without_security_data(self):
        data = {'email': 'alice.bloggs@example.com'}
        response = self.client.post(
            reverse("inviteme-post-form"), data=data)
        self.assertNotContains(
            response, "Please correct the error below", status_code=400)
        
    def test_post_with_security_data_and_empty_required_fields(self):
        data = {'timestamp':     self.timestamp,
                'security_hash': self.security_hash,
                'email':         ''}
        response = self.client.post(
            reverse("inviteme-post-form"), data=data)        
        self.assertContains(response, "Please correct the error below")
        self.assertTemplateUsed(response, "inviteme/preview.html")

    def test_signal_receiver_may_kill_the_process(self):
        # Test that receivers of signal confirmation_will_be_requested may
        # produce a ContactMailPostBadRequest (Http code 400) 
        def on_signal(sender, data, request, **kwargs):
            return False

        signals.confirmation_will_be_requested.connect(on_signal)
        self.post_valid_data() # self.response gets updated
        self.assertTemplateUsed(self.response, 
                                "inviteme/discarded.html")
        
    def test_confirmation_email_is_sent(self):
        self.assertEqual(len(mail.outbox), 0)
        self.post_valid_data() # self.response gets updated
        self.assertEqual(len(mail.outbox), 1)

    def test_signal_confirmation_requested_is_sent(self):
        self.calls = 0
        def on_signal(sender, data, request, **kwargs):
            self.calls += 1

        signals.confirmation_requested.connect(on_signal)
        self.post_valid_data() # self.response gets updated
        self.assert_(self.calls == 1)

    def test_user_is_told_about_confirmation_email_sent(self):
        self.post_valid_data() # self.response gets updated
        self.assertTemplateUsed(self.response, 
                                "inviteme/confirmation_sent.html")


class ConfirmMailViewTestCase(TestCase):

    def setUp(self):
        self.response = self.client.get(reverse("inviteme-get-form"))
        for context in self.response.context:
            if context.has_key("form"):
                form = context.get("form")
                timestamp = form.initial["timestamp"]
                security_hash = form.initial["security_hash"]
        data = {'timestamp':     timestamp,
                'security_hash': security_hash,
                'email':         'alice.bloggs@example.com'}
        self.response = self.client.post(
            reverse("inviteme-post-form"), data=data)        
        if mail_sent_queue.get(block=True):
            pass
        self.url = re.search(r'http://[\S]+', mail.outbox[0].body).group()

    def get_confirm_mail_url(self, key):
        self.response = self.client.get(reverse("inviteme-confirm-mail",
                                                kwargs={'key': key}))

    def test_404_on_bad_signature(self):
        key = self.url.split("/")[-1]
        key = key[:-1]
        self.get_confirm_mail_url(key)
        self.assertContains(self.response, "404", status_code=404)

    def test_consecutive_confirmation_url_visits_fail(self):
        # test that consecutives visits to the same confirmation URL produce
        # an Http 404 code, as the contact_msg has already been verified in
        # first visit
        key = self.url.split("/")[-1]        
        self.get_confirm_mail_url(key)
        self.get_confirm_mail_url(key)
        self.assertContains(self.response, "404", status_code=404)

    def test_signal_receiver_avoids_mailing_admins(self):
        # test that receivers of signal confirmation_received may return False
        # and thus rendering a template_discarded uotput
        def on_signal(sender, data, request, **kwargs):
            return False

        self.assertEqual(len(mail.outbox), 1) # sent during setUp
        signals.confirmation_received.connect(on_signal)
        key = self.url.split("/")[-1]
        self.get_confirm_mail_url(key)
        self.assertEqual(len(mail.outbox), 1) # mailing avoided by on_signal
        self.assertTemplateUsed(self.response, 
                                "inviteme/discarded.html")

    def test_contact_msg_is_created_and_email_sent(self):
        key = self.url.split("/")[-1]
        self.get_confirm_mail_url(key)
        data = signed.loads(key, extra_key=INVITEME_SALT)
        try:
            cmail = ContactMail.objects.get(email=data["email"], 
                                            submit_date=data["submit_date"])
        except:
            cmail = None
        self.assert_(cmail != None)
        # be sure that settings module contains either ADMINS or 
        # CONTACTME_NOTIFY_TO, otherwise there won't be 2 mails
        self.assertEqual(len(mail.outbox), 2)

    def test_user_is_told_about_contact_msg_received(self):
        key = self.url.split("/")[-1]
        self.get_confirm_mail_url(key)
        self.assertTemplateUsed(self.response, 
                                "inviteme/accepted.html")
