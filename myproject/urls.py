from django.contrib import admin
from django.urls import path
from django.urls import include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('mainapp/', include('mainapp.urls')),
    path('', RedirectView.as_view(url='mainapp/', permanent=True)),
    path('accounts/', include('django.contrib.auth.urls')),


]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

