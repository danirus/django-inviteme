from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('inviteme.views',
    url(r'^$',                       'get_form',     name='inviteme-get-form'),
    url(r'^post/$',                  'post_form',    name='inviteme-post-form'),
    url(r'^confirm/(?P<key>[^/]+)$', 'confirm_mail', name='inviteme-confirm-mail'),
)
