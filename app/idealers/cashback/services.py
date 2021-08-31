from typing import Dict

import requests
from django.conf import settings
from rest_framework import status


class CashbackService:
    @staticmethod
    def get_accumulated_cashback(cpf: str):
        """
        Returns the accumulated cashback value from external API
        """
        headers = {
            settings.EXTERNAL_CASHBACK_API_TOKEN_HEADER: settings.EXTERNAL_CASHBACK_API_TOKEN
        }

        response = requests.get(
            settings.EXTERNAL_CASHBACK_API,
            params={'cpf': cpf},
            headers=headers
        )

        response_data: Dict = response.json()

        if response.status_code == status.HTTP_200_OK:
            return response_data['body']
        else:
            {'credit': 0}
