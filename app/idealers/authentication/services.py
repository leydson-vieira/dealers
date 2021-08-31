from django.db.models import Q

from .exceptions import DealerAlreadyExists
from .models import Dealer


class DealerService:
    @staticmethod
    def create_dealer(full_name: str, cpf: str, email: str, password: str) -> Dealer:
        if Dealer.objects.filter(Q(email=email) | Q(cpf=cpf)).exists():
            raise DealerAlreadyExists()
        return Dealer.objects.create_user(full_name, email, password, cpf)
