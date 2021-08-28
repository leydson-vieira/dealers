import uuid

from django.db import models


class Order(models.Model):
    """"
    DB Model used to place orders created by Dealers
    """
    class Status(models.TextChoices):
        IN_VALIDATION = 'in_validation', 'Em Validação'
        APPROVED = 'approved', 'Aprovado'
        REJECTED = 'tejected', 'Rejeitado'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    code = models.CharField(max_length=150, )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    status = models.CharField(
        max_length=13,
        choices=Status,
        default=Status.IN_VALIDATION,
    )

    dealer = models.ForeignKey(
        'authentication.Dealer',
        on_delete=models.DO_NOTHING,
        to_field='cpf',
        related_name='orders',
    )

    def __str__(self) -> str:
        return f'Order: {self.id}'
