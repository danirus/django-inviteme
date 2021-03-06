.. _ref-templates:

=========
Templates
=========

List of template files coming with Django-ContactMe.

**inviteme/contactme.html**
    Entry point for the Django-ContactMe form. Template rendereded when visiting the ``/contact/`` URL. It makes use of the ``render_contact_form`` templatetag (see :doc:`templatetags`).

**inviteme/form.html**
    Used by the templatetag ``render_contact_form`` (see :doc:`templatetags`).

**inviteme/preview.html**
    Rendered either when the contact form has errors or when the user click on the ``preview`` button.

**inviteme/confirmation_email.txt**
    Email message sent to the user when the contact form is clean, after the user clicks on the ``post`` button.

**inviteme/confirmation_sent.html**
    Rendered if the contact form is clean when the user clicks on the ``post`` button and right after sending the confirmation email.

**inviteme/discarded.html**
    Rendered if a receiver of the ``confirmation_received`` signal returns False. The signal ``confirmation_received`` is sent when the user click on the URL sent by email to confirm the contact message. See :doc:`signals`. 

**inviteme/accepted.html**
    Rendered when the user click on the URL sent by email to confirm the contact message. If there are no receivers of the signal ``confirmation_received`` or none of the receivers returns False, the template is rendered and a ``ContactMsg`` model instance is created.
