.. _ref-settings:

========
Settings
========

This is the comprehensive list of settings django-inviteme recognizes.


``INVITEME_SALT``
=================

**Optional**

This setting establish the ASCII string extra_key used by ``signed.dumps`` to salt the contact form hash. As ``signed.dumps`` docstring says, just in case you're worried that the NSA might try to brute-force your SHA-1 protected secret.

An example::

     INVITEME_SALT = 'G0h5gt073h6gH4p25GS2g5AQ25hTm256yGt134tMP5TgCX$&HKOYRV'

Defaults to an empty string.


``INVITEME_NOTIFY_TO``
======================

**Optional**

This setting establish the email address that will be notified on new contact messages. May be a list of email addresses separated by commas.

An example::

     INVITEME_NOTIFY_TO = 'Alice <alice@example.com>, Joe <joe@example.com>'

Defaults to ``settings.ADMINS``.
