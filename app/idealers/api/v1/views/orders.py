from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from orders.exceptions import (DealerDoesNotExist, OrderCodeAlreadyExists,
                               OrderDoesNotExist, StatusNotAllowed)
from orders.serializers import (OrderCreateSerializer, OrderListSerializer,
                                OrderUpdateSerializer)
from orders.services import OrderService


class OrderView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs) -> Response:
        limit = request.query_params.get("limit", '')
        offset = request.query_params.get("offset", '')

        limit = int(limit) if limit.isdigit() else 10
        offset = int(offset) if offset.isdigit() else 0

        orders = OrderService.list_orders(request.user, limit, offset)
        serializer = OrderListSerializer(instance=orders, many=True)
        return Response(data=serializer.data)

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

    def patch(self, request, *args, **kwargs) -> Response:
        order_id: str = kwargs.get('order_id')

        serializer = OrderUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            order = OrderService.update_order(
                order_id=order_id, **serializer.validated_data
            )
        except OrderCodeAlreadyExists:
            return Response(
                {'detail': 'Order code already exists.'},
                status=status.HTTP_409_CONFLICT,
            )
        except OrderDoesNotExist:
            return Response(
                {'detail': 'Order not found.'},
                status=status.HTTP_404_NOT_FOUND,
            )
        except StatusNotAllowed:
            return Response(
                {'detail': 'Only in validation orders can be updated.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        list_serializer = OrderListSerializer(instance=order)
        return Response(data=list_serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs) -> Response:
        order_id: str = kwargs.get('order_id')

        try:
            OrderService.delete_order(order_id)
        except OrderDoesNotExist:
            return Response(
                {'detail': 'Order not found.'},
                status=status.HTTP_404_NOT_FOUND,
            )
        except StatusNotAllowed:
            return Response(
                {'detail': 'Only in validation orders can be deleted.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(status=status.HTTP_200_OK)


order_view = OrderView.as_view()
