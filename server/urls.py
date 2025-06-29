from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('djangoadmin/', admin.site.urls),
    path('',include('app.urls')),
    path('',include('api.urls')),
    path('',include('marquee.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)