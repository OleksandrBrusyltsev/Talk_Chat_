from django.db.models import Q
from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from authentication.utils import CustomPageNumberPagination
from channels.models import Channel
from channels.serializers import ChannelSerializer


# Create your views here.

class ChannelListCreateView(generics.ListCreateAPIView):
    """ API endpoint for listing and creating channels """

    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        image_file = self.request.data.get('image')

        if image_file:
            channel = serializer.save(owner=self.request.user, image=image_file)
        else:
            default_public_id = "profile_photos/def_chat_pa7kfg"
            channel = serializer.save(owner=self.request.user, image=default_public_id)

        return channel


class ChannelRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """API endpoint for retrieving, updating, and deleting a channel"""

    serializer_class = ChannelSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        return Channel.objects.all()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Channel been deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


class ChannelsByOwnerListView(generics.ListAPIView):

    """ API endpoint for listing channels by owner"""

    serializer_class = ChannelSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        owner_id = self.request.query_params.get('owner_id')
        if owner_id:
            return Channel.objects.filter(owner_id=owner_id).select_related('owner')
        return Channel.objects.all()


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def channels_for_authenticated_owner(request):
    """ API endpoint to retrieve channels owned by an authenticated user."""
    owner = request.user
    channels = Channel.objects.filter(owner=owner).select_related('owner')

    paginator = CustomPageNumberPagination()
    paginated_channels = paginator.paginate_queryset(channels, request)

    serializer = ChannelSerializer(paginated_channels, many=True)
    return paginator.get_paginated_response(serializer.data)


class ChannelSearchView(generics.ListAPIView):
    """API endpoint for searching channels based on a query."""

    serializer_class = ChannelSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        search_query = self.request.query_params.get('search')
        if search_query:
            query = Q(title__icontains=search_query) | Q(title__istartswith=search_query)
            return Channel.objects.filter(query)
        return Channel.objects.none()
