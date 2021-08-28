from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _


class DealerManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, full_name, email, password, cpf, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError('Email field is required')
        if not cpf:
            raise ValueError('Cpf field is required')

        email = self.normalize_email(email)
        user = self.model(full_name=full_name, email=email, cpf=cpf, **extra_fields)
        user.set_password(password)
        user.save()
        return user