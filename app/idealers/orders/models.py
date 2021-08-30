import uuid

from django.db import models


class Order(models.Model):
    """"
    DB Model used to place orders created by Dealers
    """
    class Status(models.TextChoices):
        IN_VALIDATION = 'in_validation', 'Em Validação'
        APPROVED = 'approved', 'Aprovado'
        REJECTED = 'rejected', 'Rejeitado'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    code = models.CharField(max_length=150, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    status = models.CharField(
        max_length=13,
        choices=Status.choices,
        default=Status.IN_VALIDATION,
    )

    dealer = models.ForeignKey(
        'authentication.Dealer',
        on_delete=models.DO_NOTHING,
        related_name='orders',
    )
