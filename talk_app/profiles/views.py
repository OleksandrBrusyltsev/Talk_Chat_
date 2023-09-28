from tokenize import TokenError

from rest_framework import generics, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken

from authentication.models import CustomUser
from profiles.serializers import ChangePasswordAccountSerializer, ProfileUpdateSerializer


class ChangePasswordView(generics.UpdateAPIView):
    """API endpoint for change  password  profile"""

    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordAccountSerializer

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(instance=self.request.user, data=request.data)
        serializer.is_valid(raise_exception=True)

        old_password = serializer.validated_data.get('old_password')

        if not self.request.user.check_password(old_password):
            return Response({"message": "your current password is incorrect"},
                            status=status.HTTP_400_BAD_REQUEST)

        self.request.user.set_password(serializer.validated_data['password'])
        self.request.user.save()

        return Response({"message": "Password has been changed successfully."},
                        status=status.HTTP_200_OK)


class ProfileUpdateView(APIView):
    """ API endpoint for updating a user's profile."""

    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]


    def put(self, request, *args, **kwargs):
        user_profile = CustomUser.objects.get(id=request.user.id)
        serializer = ProfileUpdateSerializer(user_profile, data=request.data)

        if serializer.is_valid():
            serializer.save()


            updated_user = CustomUser.objects.get(id=request.user.id)
            updated_data = {
                "message": "Profile information has been updated successfully.",
                "username": updated_user.username,
                "profile_photo": self.request.build_absolute_uri(
                    updated_user.profile_photo.url) if updated_user.profile_photo else None
            }

            return Response(updated_data, status=200)
        else:
            return Response(serializer.errors, status=400)


class DeleteAccountView(APIView):
    """ API endpoint for deleting a user's account."""

    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        user = request.user
        user.delete()
        return Response({"message": "Account has been deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


class RefreshUser(APIView):
    """ For reset page """

    def post(self, request):
        refresh_token = request.data.get('refresh')

        if not refresh_token:
            return Response({'error': 'Refresh token is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            refresh_token = RefreshToken(refresh_token)
            user_id = refresh_token['user_id']
            user = CustomUser.objects.get(pk=user_id)

            if user.profile_photo:
                profile_photo_url = request.build_absolute_uri(user.profile_photo.url)
            else:
                profile_photo_url = None

            return Response({
                'user_id': user.id,
                'username': user.username,
                'email': user.email,
                'profile_photo': profile_photo_url
            }, status=status.HTTP_200_OK)

        except TokenError:
            raise AuthenticationFailed('Invalid refresh token.', code='invalid_refresh_token')


