.. _ref-templatetags:

============
Templatetags
============

Django-inviteme has a templatetag to render the contact form.

``render_contact_form``
=======================

Sites may use a hidden div that fadeIn/slideUp when clicking on **request an invitation** link. Use the ``render_mail_form`` templatetag to render the mail form. The ``inviteme/form.html`` template will then be used to render the form.
