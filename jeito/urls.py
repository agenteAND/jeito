from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('dashboard.urls', namespace='dashboard')),
    url(r'^', include('core.urls')),
    url(r'^members/', include('members.urls', namespace='members')),
    url(r'^booking/', include('booking.urls', namespace='booking')),
    url(r'^accounting/', include('accounting.urls', namespace='accounting')),
    url(r'^tracking/', include('tracking.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if 'docs' in settings.INSTALLED_APPS:
    urlpatterns += [
        url(r'^docs/', include('docs.urls', namespace='docs')),
    ]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
