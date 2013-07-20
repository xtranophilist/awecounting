from django.contrib.auth import get_user_model
from django.core.validators import email_re

class BasicBackend:
    def get_user(self, user_id):
        try:
            return get_user_model().objects.get(pk=user_id)
        except get_user_model.DoesNotExist:
            return None

class EmailOrUsernameBackend(BasicBackend):
    def authenticate(self, username=None, password=None):
        #If username is an email address, then try to pull it up
        if email_re.search(username):
            try:
                user = get_user_model().objects.get(email=username)
            except get_user_model().DoesNotExist:
                return None
        else:
            #We have a non-email address username we should try username
            try:
                user = get_user_model().objects.get(username=username)
            except get_user_model().DoesNotExist:
                return None
        if user.check_password(password):
            return user
