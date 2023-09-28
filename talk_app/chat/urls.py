

from django.urls import path

from . import views
#
# urlpatterns = [
#     path("", views.index, name="index"),
#     path("room/<int:pk>/", views.room, name="room"),
#     path('websocket-url/', WebSocketURLView.as_view(), name='websocket-url')
#
# ]


urlpatterns = [
    path("", views.lobby),

]