from django.conf.urls import include, patterns, url
from django.contrib import admin
from authentication import views as authview
from .settings import STATIC_ROOT
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

admin.autodiscover()

urlpatterns = patterns('',
	url(r'^admin/', include(admin.site.urls)), 
	url(r'^login/$', authview.login_user, name="login"), 
)

urlpatterns += patterns('',
	url(r'^static/(.*)$', 'django.views.static.serve', {'document_root': STATIC_ROOT, 'show_indexes': True}),
)
