from django.contrib import admin
from django.urls import path, include

from channels.views import ChannelListCreateView, ChannelRetrieveUpdateDestroyView, ChannelsByOwnerListView, \
    channels_for_authenticated_owner, ChannelSearchView

urlpatterns = [
    path('api/v1/channels/', ChannelListCreateView.as_view(), name='channel-list-create'),
    path('api/v1/channels/<int:pk>/', ChannelRetrieveUpdateDestroyView.as_view(), name='channel-detail'),
    path('api/v1/channels/owner_all/', ChannelsByOwnerListView.as_view(), name='channels-by-owner-list-all'),
    path('api/v1/channels_only_owner/', channels_for_authenticated_owner, name='channels-only-owner'),
    path('api/v1/channels/<int:pk>/', ChannelRetrieveUpdateDestroyView.as_view(),
         name='channel-retrieve-update-destroy'),
    path('api/v1/channels/search/', ChannelSearchView.as_view(), name='channel-search'),
]
