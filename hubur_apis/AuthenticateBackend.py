from django.conf import settings
from django.contrib.auth import get_user_model, backends
from django.db.models import Q

class EmailModelBackend(backends.BaseBackend):
    """  Authenticate User with Contact OR Email """
    USER_MODEL = get_user_model()


    def authenticate(self, request, **kwargs):
        custom_kwargs = {}
        if 'email' in kwargs:
            username = kwargs.get("email")
        else:
            username = kwargs.get("username")
        password = kwargs.get("password")
        if '@' in username:
            custom_kwargs = Q(email=username.lower())
        else:
            custom_kwargs = Q(username=username)
        try:
            user = self.USER_MODEL.objects.get(custom_kwargs)
        except self.USER_MODEL.DoesNotExist:
            return None

        if user.check_password(password) and user.is_active:
            return user
        return None
    
    def get_user(self, user_id):
        try:
            return self.USER_MODEL.objects.get(pk=user_id)
        except self.USER_MODEL.DoesNotExist:
            return None