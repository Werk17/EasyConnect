from os import name
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('profile/', include('Easyconnect.urls'), name='profile'),
    path('', include('EasyConnect.urls')),
    path('', include('customuser.urls')),
    path('', include('ContactUs.urls')),
    path('logs/', include('log_viewer.urls')),
    path('chat/', include('chat.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
