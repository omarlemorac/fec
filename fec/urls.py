from django.conf.urls import include, patterns, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from authentication import views as authview

admin.autodiscover()

urlpatterns = patterns('',
	url(r'^admin/', include(admin.site.urls)), 
	url(r'^login/$', authview.login_user, name="login"), 
)

if not settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns += patterns('django.views.static', r'^media/(?P<path>.*)', 'serve', {'document_root': settings.MEDIA_ROOT})
