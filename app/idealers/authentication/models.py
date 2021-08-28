import uuid

from django.contrib.auth.base_user import AbstractBaseUser

from django.utils import timezone
from django.db import models

from .managers import DealerManager


class Dealer(AbstractBaseUser):
    """
    DB Model used to authenticate users (or dealers)
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    full_name = models.CharField(max_length=150)
    cpf = models.CharField(max_length=14, unique=True)
    email = models.EmailField(max_length=150, null=False, blank=False, unique=True)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = DealerManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['cpf']

    def __str__(self) -> str:
        return f'User: {self.email}'
