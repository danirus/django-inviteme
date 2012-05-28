.. django-inviteme documentation master file, created by
   sphinx-quickstart on Sat Dec 10 00:09:54 2011.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Introduction
============

**Django-inviteme** provides a simple contact form that only hits the database 
after the user confirm her email address. It sends threaded emails to avoid response blocking.


.. toctree::
   :maxdepth: 2

   example
   tutorial
   signals
   templatetags
   settings
   templates


Quick start
===========

1. Add ``inviteme`` to ``INSTALLED_APPS``.
2. Add ``url(r'^invite/', include('inviteme.urls'))`` to your root URLconf.
3. ``syncdb``, ``runserver``, and
4. Hit http://localhost:8000/invite/ in your browser!


Workflow in short
=================

The user...

#. Clicks on the `request an invitation` link of your site.

#. She types her email address and clicks on `request`.

#. Then Django-Inviteme:

 #. Creates a token with the form data.

 #. Sends an email to her with a confirmation URL containing the token.

#. She receives the email, she opens it, and she clicks on the confirmation link.

#. Then Django-Inviteme:

 #. Check that the token is correct and creates a ``ContactEmail`` model instance.

 #. Sends an email to ``INVITEME_NOTIFY_TO`` addresses notifying that a new contact email has arrived.

 #. And shows a template being grateful to her for the message.

Read a longer workflow description in the :ref:`workflow-label` section of the Tutorial.
