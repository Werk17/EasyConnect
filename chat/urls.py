from django.urls import path, re_path

from .views import index, room

urlpatterns = [
    path('chatchoose/', index, name='index'),
    re_path(r'^(?P<room_name>[^/]+)/$', room, name='room'),
]