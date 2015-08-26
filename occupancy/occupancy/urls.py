from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()
#error
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'occupancy.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^template/',include('webApp.urls',namespace="attendance-admin")),
    url(r'^attendance/$',include('attendance.urls')),
    # url(r'^oauth/', include ('oauth_provider.urls')),
    url('', include('django.contrib.auth.urls', namespace='auth')),
)

