import time

from django.test import TestCase

from inviteme.forms import ContactMailSecurityForm, ContactMailForm


class ContactMailSecurityFormTestCase(TestCase):

    def test_constructor(self):
        # timestamp and security_hash calculated during construction
        form = ContactMailSecurityForm()
        self.assert_(form.initial.get("timestamp",     None) != None)
        self.assert_(form.initial.get("security_hash", None) != None)
        self.assert_(form.initial.get("honeypot",      None) == None)

        # even though they were provided as initial data
        initial = {'timestamp':'1122334455', 'security_hash':'blahblahashed'}
        form = ContactMailSecurityForm(initial=initial.copy())
        self.assert_(form.initial["timestamp"]     != initial["timestamp"])
        self.assert_(form.initial["security_hash"] != initial["security_hash"])

    def test_clean_timestamp(self):
        # check that a timestamp more than two hours old is not accepted
        form = ContactMailSecurityForm()
        timestamp = int(form.initial["timestamp"]) - (2 * 60 * 61)
        security_hash = form.generate_security_hash(timestamp)
        data = {"timestamp":str(timestamp), "security_hash":security_hash}
        form = ContactMailSecurityForm(data=data)
        self.assert_(form.errors.get("timestamp", None) != None)

    def test_clean_security_hash(self):
        # check that changing the timestamp invalidates the security_hash
        form = ContactMailSecurityForm()
        data = {"timestamp": str(time.time()), 
                "security_hash": form.initial["security_hash"]}
        form = ContactMailSecurityForm(data=data)
        self.assert_(form.errors.get("security_hash", None) != None)
        
    def test_clean_honeypot(self):
        # check that validation error raises when honeypot is not empty
        form = ContactMailSecurityForm()
        data = {"honeypot": "Oh! big mistake!"}
        data.update(form.initial)
        form = ContactMailSecurityForm(data=data)
        self.assert_(form.errors.get("honeypot", None) != None)
        

EMAIL_ADDR = "alice.liddell@wonderland.com"

        
class ContactMailFormTestCase(TestCase):

    def test_get_instance_data(self):
        # check get_contact_msg raises ValueError when form is not valid
        form = ContactMailForm()
        email = 'jane.bloggs@example.com'
        data = {'email': email}
        data.update(form.initial)
        form = ContactMailForm(data=data)
        form.is_valid()
        data = form.get_instance_data()
        self.assert_( len(data) == 2 )
        self.assert_( email   == data['email'] )
