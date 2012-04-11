from django.conf.urls.defaults import patterns, include

urlpatterns = patterns('',
    (r'^invite/', include('inviteme.urls')),
)
