from django.conf.urls import include, patterns, url
from django.contrib import admin
from fec.views import BdView


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^db/$', BdView.as_view(), name="showDB")
)
