from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from inviteme.models import ContactMail

class ContactMailAdmin(admin.ModelAdmin):
    list_display = ('email', 'ip_address', 'submit_date')
    fieldsets = (
        (None,          {'fields': ('site',)}),
        (_('Content'),  {'fields': ('email','submit_date', 'ip_address')}),
    )
    date_hierarchy = 'submit_date'
    ordering = ('-submit_date',)

admin.site.register(ContactMail, ContactMailAdmin)
