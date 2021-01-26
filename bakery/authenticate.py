from .models import *


class AuthBackend(object):
    supports_object_permissions = True
    supports_anonymous_user = False
    supports_inactive_user = False

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    def authenticate(self, email, password):
        try:
            user = User.objects.get(
                email=email, is_active=True
            )
        except User.DoesNotExist:
            return None

        return user if user.check_password(password) else None

    def get_user_by_email(self, email):
        try:
            user = User.objects.get(
                email=email
            )

            return user
        except User.DoesNotExist:
            return None
