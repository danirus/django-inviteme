import datetime

from django.db import models
from django.conf import settings
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _


class ContactMail(models.Model):
    """
    An incoming message from a site visitor.
    """
    site = models.ForeignKey(Site)
    email = models.EmailField(_("Contact's email address"), primary_key=True)
    submit_date = models.DateTimeField(_("Date/Time submitted"), default=None)
    ip_address  = models.IPAddressField(_('IP address'), blank=True, null=True)
    
    class Meta:
        db_table = "inviteme_contact_mail"
        ordering = ('submit_date',)
        verbose_name = _('contact mail')
        verbose_name_plural = _('contact mails')

    def __unicode__(self):
        return "%s" % self.email

    def save(self, *args, **kwargs):
        if self.submit_date is None:
            self.submit_date = datetime.datetime.now()
        super(ContactMail, self).save(*args, **kwargs)
