from django.db import models


class Cashback(models.Model):
    """"
    DB Model used to save Cashback records and its values
    """
    order = models.OneToOneField(
        'orders.Order',
        on_delete=models.CASCADE,
        primary_key=True
    )

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    percentage = models.DecimalField(max_digits=3, decimal_places=2)
