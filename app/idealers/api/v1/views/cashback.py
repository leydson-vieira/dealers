from typing import Dict
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from cashback.serializers import AccumulatedCashbackSerializer
from cashback.services import CashbackService


class CashbackView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs) -> Response:
        accumulated_cashback: Dict = CashbackService.get_accumulated_cashback(
            request.user.cpf
        )

        serializer = AccumulatedCashbackSerializer(data=accumulated_cashback)
        serializer.is_valid(raise_exception=True)

        return Response(data=serializer.validated_data, status=status.HTTP_200_OK)


cashback_view = CashbackView.as_view()
