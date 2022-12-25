"""
Views for the user API.
"""
from django.contrib.auth import authenticate
from rest_framework import (
    generics,
    # authentication,
    permissions, status
)
from django.conf import settings
from django.urls import reverse
from django.core.mail import send_mail
from rest_framework.settings import api_settings
from rest_framework.response import Response

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.dispatch import receiver
from django_rest_passwordreset.signals import reset_password_token_created
from user.serializers import (
    UserSerializer
)


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system."""
    serializer_class = UserSerializer


class CreateTokenView(TokenObtainPairView):
    """Create a new auth token for user."""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(
                email=email,
                password=password,
            )
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh_token": str(refresh),
                "access_token": str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        return Response({
            "error": "Invalid Username/Password"
        }, status=status.HTTP_400_BAD_REQUEST)


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user."""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Retrieve and return the authenticated user."""
        return self.request.user


@receiver(reset_password_token_created)
def password_reset_token_created(
    sender, instance, reset_password_token, *args, **kwargs
):
    """Doing a proxy call so this lands on the MQ"""
    base = "http://localhost:8041"
    email_plaintext_message = "{}{}?token={}".format(
        base,
        reverse("user:api-password-reset:reset-password-request"),
        reset_password_token.key,
    )

    send_mail(
        "Password Reset for {title}".format(title="Sample CRUD"),
        email_plaintext_message,
        settings.EMAIL_HOST_USER,
        [reset_password_token.user.email],
    )

# Create your views here.
