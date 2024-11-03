from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
import logging
from django.contrib import messages

logger = logging.getLogger(__name__)

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()

        try:
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            logger.debug(f"No user found with email: {username}")
            if request:
                messages.error(request, "No account found with this email.")
            return None

        if user.check_password(password):
            return user

        logger.debug("Password mismatch.")
        if request:
            messages.error(request, "Incorrect password.")
        return None