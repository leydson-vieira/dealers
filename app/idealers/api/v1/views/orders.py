from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from orders.serializers import OrderCreateSerializer
from orders.services import OrderService
from orders.exceptions import DealerDoesNotExist, OrderCodeAlreadyExists


class OrderView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs) -> Response:
        serializer: OrderCreateSerializer = OrderCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            OrderService.create_order(**serializer.validated_data)
        except OrderCodeAlreadyExists:
            return Response(
                {'detail': 'Order code already exists.'},
                status=status.HTTP_409_CONFLICT,
            )
        except DealerDoesNotExist:
            return Response(
                {'detail': 'Dealer with this CPF does not exist.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(status=status.HTTP_201_CREATED)


order_view = OrderView.as_view()