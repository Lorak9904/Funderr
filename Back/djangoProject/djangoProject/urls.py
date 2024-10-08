
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from register import views as v

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('django.contrib.auth.urls')),
    path('register/', v.register, name="register"),
    path('', include('funderr.urls')),
    path('accounts/', include('django.contrib.auth.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
