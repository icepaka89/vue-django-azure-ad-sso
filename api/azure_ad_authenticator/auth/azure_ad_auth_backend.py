from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from azure_ad_authenticator.auth.helpers.graph_helper import *

class AzureAdAuthBackend(BaseBackend):
    '''
    This backend handles user authentication when provided a valid Azure AD access token
    '''
    
    def authenticate(self, request, token=None):
        # Get the user's profile
        msgraph_user = get_user(token)
        
        # True if the MS Graph API actually returned a user from the access token
        is_user_valid = 'userPrincipalName' in msgraph_user and not 'error' in msgraph_user

        # If user authentication succeeded, then get that user from the database,
        # or create a new user if this is their first time logging in, and then
        # return the authenticated user
        if is_user_valid:
            try:
                user = User.objects.get(username=msgraph_user['userPrincipalName'])
            except User.DoesNotExist:
                new_user = User(username=msgraph_user['userPrincipalName'])
                new_user.is_staff = True
                new_user.is_superuser = False
                new_user.save()

            return User.objects.get(username=msgraph_user['userPrincipalName'])
        
        # Return None if the user authentication failed
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
