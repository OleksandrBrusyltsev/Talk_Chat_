from django.contrib.auth import get_user_model
from django.core.files import File
from django.core.mail import send_mail
from django.shortcuts import  redirect
from django_rest_passwordreset.models import ResetPasswordToken
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from authentication.serializers import UsernameRegisterSerializer, EmailLoginSerializer
from authentication.utils import send_account_confirmation_email, is_expired_decorator
from authentication.constans import DEFAULT_PROFILE_PHOTO_FILENAME, FRONT_URL, RESET_PASSWORD_URL, FROM_EMAIL
from talk_core import settings
import os

# Create your views here.
class UserRegistrationAPIView(APIView):
    """Registration user """

    def post(self, request):
        """Processing registration form data and creating a new user"""
        serializer = UsernameRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        CustomUser = get_user_model()

        if CustomUser.objects.filter(username=username).exists() or CustomUser.objects.filter(email=email).exists():
            return Response({"message": "A user with this email already exists."},
                            status=status.HTTP_400_BAD_REQUEST)

        user = CustomUser.objects.create_user(username=username, email=email, is_active=False)

        with open(os.path.join(settings.MEDIA_ROOT, DEFAULT_PROFILE_PHOTO_FILENAME), 'rb') as f:
            user.profile_photo.save(DEFAULT_PROFILE_PHOTO_FILENAME, File(f))

        user.set_password(password)
        user.save()

        """Send an account confirmation email"""
        send_account_confirmation_email(email, user.id)

        return Response({"user": serializer.data,
                         "message": "Registration was successful. Check your email to confirm your account."},
                        status=status.HTTP_201_CREATED)


@api_view(['GET'])
def confirm_account(request, user_id):
    """API endpoint to confirm a user's account."""

    User = get_user_model()

    try:
        user = User.objects.get(pk=user_id)
        if not user.is_active:
            user.is_active = True
            user.save()

            return redirect(FRONT_URL)
        else:
            return Response({"message": "The account has already been confirmed previously."},
                            status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        return Response({"message": "Account not found."}, status=status.HTTP_404_NOT_FOUND)


class EmailLoginAPIView(APIView):
    """Custom class for login with email """

    def post(self, request):
        serializer = EmailLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            User = get_user_model()
            user = User.objects.filter(email=email).first()

            if user and user.check_password(password):
                refresh = RefreshToken.for_user(user)
                response_data = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'username': str(user.username),
                    'email': str(user.email),
                    'user_id': str(user.id)
                }

                if user.profile_photo:

                    profile_photo_url = request.build_absolute_uri(user.profile_photo.url)
                    response_data['profile_photo'] = profile_photo_url
                else:
                    response_data['profile_photo'] = "Photo doesnt not found"

                return Response(response_data)
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class PasswordResetAPIView(APIView):
    """
       API view to handle the password reset request.

       This view sends a password reset email to the user's email address
       with a link containing a reset token.

   """

    def post(self, request):
        email = request.data.get('email')

        try:
            user = get_user_model().objects.get(email=email)
        except get_user_model().DoesNotExist:
            return Response({"message": "User with this email does not exist."}, status=status.HTTP_404_NOT_FOUND)

        reset_token = ResetPasswordToken.objects.create(user=user)

        reset_url = RESET_PASSWORD_URL + reset_token.key
        message = f'To reset your password, follow this link: {reset_url}'
        from_email = FROM_EMAIL
        to_email = email
        send_mail('Password Reset', message, from_email, [to_email])

        return Response({"message": "Password reset email has been sent. Check your email to reset your password."},
                        status=status.HTTP_200_OK)


@is_expired_decorator
class PasswordResetConfirmAPIView(APIView):
    """
        API view to handle the password reset confirmation.

        This view confirms the password reset by validating the reset token,
        updating the user's password, and deleting the used token.

    """

    def post(self, request):
        token = request.data.get('token')
        new_password = request.data.get('new_password')

        try:
            reset_token = ResetPasswordToken.objects.get(key=token)

        except ResetPasswordToken.DoesNotExist:
            return Response({"message": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)

        if reset_token.is_expired():
            return Response({"message": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)

        user = reset_token.user
        user.set_password(new_password)
        user.save()

        reset_token.delete()

        return Response({"message": "Password has been reset successfully."}, status=status.HTTP_201_CREATED)
