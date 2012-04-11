from django import template
from django.template.loader import render_to_string

from inviteme.forms import ContactMailForm

register = template.Library()


class MailFormNode(template.Node):
    def render(self, context):
        context.push()
        form_str = render_to_string("inviteme/form.html", 
                                    {"form": ContactMailForm() }, 
                                    context)
        context.pop()
        return form_str


def render_mail_form(parser, token):
    """
    Render the contact form (as returned by ``{% render_mail_form %}``) 
    through the ``inviteme/form.html`` template.

    Syntax::

        {% render_mail_form %}
    """
    return MailFormNode()

register.tag(render_mail_form)
