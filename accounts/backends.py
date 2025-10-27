from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q


class EmailOrUsernameModelBackend(ModelBackend):
    """
    Custom authentication backend that allows users to log in with either
    their username or email address.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Authenticate a user based on username or email.
        
        Args:
            request: The HTTP request object
            username: Username or email provided by the user
            password: Password provided by the user
            **kwargs: Additional keyword arguments
            
        Returns:
            User object if authentication succeeds, None otherwise
        """
        UserModel = get_user_model()
        
        if username is None or password is None:
            return None
        
        try:
            # Try to fetch the user by searching the username OR email field
            user = UserModel.objects.get(
                Q(username__iexact=username) | Q(email__iexact=username)
            )
        except UserModel.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user
            UserModel().set_password(password)
            return None
        except UserModel.MultipleObjectsReturned:
            # If multiple users exist with the same email (shouldn't happen
            # with proper unique constraints), return None
            return None
        
        # Check if the password is correct
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        
        return None
