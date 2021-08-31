from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.exceptions import DealerAlreadyExists
from authentication.serializers import DealerCreateSerializer
from authentication.services import DealerService


class DealerView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs) -> Response:
        serializer: DealerCreateSerializer = DealerCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            DealerService.create_dealer(**serializer.validated_data)
        except DealerAlreadyExists:
            return Response(
                {'detail': 'Dealer already exists.'},
                status=status.HTTP_409_CONFLICT,
            )

        return Response(status=status.HTTP_201_CREATED)


dealer_view = DealerView.as_view()